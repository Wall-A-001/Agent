import numpy as np
from gym import spaces
from ..miniworld import MiniWorldEnv, Room
from ..entity import Box, Agent
from ..params import DEFAULT_PARAMS
from ..math import *
import random

class HAWKMaze(MiniWorldEnv):
    """
    HAWK-Maze zum Trainieren eines DDQ-Agents
    """

    def __init__(self, **kwargs):
        "------Parameter-Einstellungen-------"

        max_steps = 300
        domain_rand = False

        # Maze
        self.num_rows = 3               # Zeilen des HAWK-Mazes
        self.num_cols = 3               # Spalten des HAWK-Mazes
        self.room_size = 5              # Raumgröße
        self.gap_size = 0.25            # Wanddicke/Abstand zwischen 2 Räumen

        # Agent
        self.agent_groesse = 0.6        # Radius Agent (für Kollisionsmodell/Aufheben-Aktion)
        self.schritt_agent = 0.50       # Schrittweite
        self.schritt_toleranz = 0.02    # Schrittweite-Toleranz, wenn Domain-Rand. aktiviert
        self.phi_agent = 45             # Drehwinkel
        self.phi_tol = 0.0              # Drehwinkel-Toleranz, wenn Domain-Rand. aktiviert
        self.start_winkel = [0, 0.5*math.pi, math.pi, -0.5*math.pi] # mögl. Start-Winkel des Agents relativ zum Env

        # Objekte
        self.anzahl_objs = 3            # wenn None oder 0: Anzahl zufällig aus (min, max)
        self.anzahl_objs_min = 1        # untere Grenze für Anzahl zufälliger Objekte
        self.anzahl_objs_max = 4        # obere Grenze für Anzahl zufälliger objekte


        "------Setzen der Parameter------"
        params = DEFAULT_PARAMS.copy()
        params.set('forward_step', self.schritt_agent, self.schritt_agent - self.schritt_toleranz, self.schritt_agent + self.schritt_toleranz)
        params.set('turn_step', self.phi_agent, self.phi_agent - self.phi_tol, self.phi_agent + self.phi_tol)

        super().__init__(
            max_episode_steps=max_steps,
            domain_rand=domain_rand,
            params=params,
            **kwargs
        )

        "------Reduzierung des Aktionsraumes------"
        # Mögliche Aktionen:
        # turn_left = 0 | turn_right = 1 | move_forward = 2 | move_back = 3 | pickup = 4
        self.action_space = spaces.Discrete(self.actions.pickup+1)

    "------Erstellung des Raumes in MiniWorld------"

    def _reward(self):
        #Ziel ist es, den Agent mit möglichst wenigen Aktionen alle verfügbaren...
        #...Objekte einsammeln zu lassen. Die Belohnung pro eingesammeltem Objekt...
        #...erhöht sich linear, da der Schwierigkeitsgrad mit weniger verbleibenden...
        #...Objekten zunimmt. Außerdem verringert jede ausgeführte Aktion die Belohnung...
        #...etwas, um die Wahl des kürzesten Weges anzustreben."
        #return 1.0 * self.num_picked_up - 0.2 * (self.step_count / self.max_episode_steps)

        # Konstante Belohnung für jedes eingesammelte Objekt. Abzug für Anzahl benötigter Aktionen
        return 1.0 - 0.2 * (self.step_count / self.max_episode_steps)

    def step(self, action):
        obs, reward, done, info = super().step(action)

        "Box einsammeln mit pick_up Aktion"
        if self.agent.carrying:
            self.entities.remove(self.agent.carrying)
            self.agent.carrying = None
            self.num_picked_up += 1
            reward = self._reward()     # Reward berechnen
            self.step_count = 0         # Timer nach erfolgreichem Aufsammeln zurücksetzen

            if self.num_picked_up == self.anzahl_objs:
                done = True             # Episode beenden nach dem letzten Objekt

        return obs, reward, done, info

    def reset(self):
        """
        Reset the simulation at the start of a new episode
        This also randomizes many environment parameters (domain randomization)
        """

        # Step count since episode start
        self.step_count = 0

        # Create the agent
        self.agent = Agent()
        self.agent.radius = self.agent_groesse      # Anpassen der Agent-Größe

        # List of entities contained
        self.entities = []

        # List of rooms in the world
        self.rooms = []

        # Wall segments for collision detection
        # Shape is (N, 2, 3)
        self.wall_segs = []

        # Generate the world
        self._gen_world()

        # Check if domain randomization is enabled or not
        rand = self.rand if self.domain_rand else None

        # Randomize elements of the world (domain randomization)
        self.params.sample_many(rand, self, [
            'sky_color',
            'light_pos',
            'light_color',
            'light_ambient'
        ])

        # Get the max forward step distance
        self.max_forward_step = self.params.get_max('forward_step')

        # Randomize parameters of the entities
        for ent in self.entities:
            ent.randomize(self.params, rand)

        # Compute the min and max x, z extents of the whole floorplan
        self.min_x = min([r.min_x for r in self.rooms])
        self.max_x = max([r.max_x for r in self.rooms])
        self.min_z = min([r.min_z for r in self.rooms])
        self.max_z = max([r.max_z for r in self.rooms])

        # Generate static data
        if len(self.wall_segs) == 0:
            self._gen_static_data()

        # Pre-compile static parts of the environment into a display list
        self._render_static()

        # Generate the first camera image
        obs = self.render_obs()

        # Return first observation
        return obs

    def _gen_world(self):
        rows = []
        # For each row
        for j in range(self.num_rows):
            row = []

            # For each column
            for i in range(self.num_cols):
                min_x = i * (self.room_size + self.gap_size)
                max_x = min_x + self.room_size

                min_z = j * (self.room_size + self.gap_size)
                max_z = min_z + self.room_size

                room = self.add_rect_room(
                    min_x=min_x,
                    max_x=max_x,
                    min_z=min_z,
                    max_z=max_z,
                    wall_tex='brick_wall',
                    floor_tex='asphalt'
                )
                row.append(room)

            rows.append(row)

        visited = set()
        'Erstellung des Labyrinths und Plazierung der Objekte + Agent'

        def visit(i, j):
            """
            Recursive backtracking maze construction algorithm
            Quelle: https://stackoverflow.com/questions/38502
            """
            'Raumproportionen auslesen'
            room = rows[j][i]

            'Wenn Nachbar schon bekannt wird Raum hinzugefügt'
            visited.add(room)

            'Nachbar nach Zufallsprinzip festlegen'
            neighbors = self.rand.subset([(0, 1), (0, -1), (-1, 0), (1, 0)], 4)

            'Für jeden möglichen Nachbarn ausführen'
            for dj, di in neighbors:
                ni = i + di
                nj = j + dj

                'Befindet sich der Nachbar im definierten Raum, soll Algorithmus fortgeführt werden'
                if nj < 0 or nj >= self.num_rows:
                    continue
                if ni < 0 or ni >= self.num_cols:
                    continue

                'Definition des Nachbarn an Zeite und Spalte orientieren'
                neighbor = rows[nj][ni]

                'Ist der Nachbar schon bekannt, Algo fortführen'
                if neighbor in visited:
                    continue

                'Alle Nachbarn gesichtet -> Nachbarn werden verbunden zu einem Labyrinth'
                if di == 0:
                    self.connect_rooms(room, neighbor, min_x=room.min_x, max_x=room.max_x)
                elif dj == 0:
                    self.connect_rooms(room, neighbor, min_z=room.min_z, max_z=room.max_z)

                'Rekursiever Aufruf der Funktion'
                visit(ni, nj)

        'Backtracking-Algo aufrühren -> Startpunkt oben Links'
        visit(0, 0)

        'Erstellen und plazieren der Objekte (Box)'
        'Boxen werden horizontal ausgerichtet'
        if self.anzahl_objs == None or self.anzahl_objs == 0:
            self.anzahl_objs = random.randint(self.anzahl_objs_min, self.anzahl_objs_max)

        for obj in range(self.anzahl_objs):
            self.box = self.place_entity(Box(color='red', size=0.9), dir=0)

        'Zähler auf 0 setzen'
        self.num_picked_up = 0

        'Plazieren des Agents'
        self.place_agent(dir=random.choice(self.start_winkel))  # rechtwinklige Ausrichtung des Agents am Maze
