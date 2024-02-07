import pygame as pg

class Node():
    def __init__(self, name, **kwargs):
        super().__init__()
        self.name = name
        self.neighbors = {}

        self.weather_penalty = {'move': 0, 'accl': 0}

        self.process_kwargs(kwargs)
        
        self.radius = 34
        if self.name == 'node0':
            self.radius = 50
        self.surf = pg.Surface((2*self.radius, 2*self.radius))
        self.surf.fill((255, 255, 255))
        self.surf.set_colorkey((255,255,255))
        self.rect = self.surf.get_rect()

        #self.surf_climbers = pg.Surface((2*self.radius, 2*self.radius))
        #self.surf_climbers.fill((255, 255, 255))
        #self.surf_climbers.set_colorkey((255,255,255))
        #self.climber_pos = [(10, 10), (40, 10), (10, 40), (40, 40)]

        self.climber_list = []
        self._highlighted = False
        self.highlight()

    def add_climber(self, climber):
        # TODO - max number of climbers (from data.py?)
        self.climber_list.append(climber)
        #self.draw_climbers()

    def remove_climber(self, climber):
        if climber in self.climber_list:
            self.climber_list.remove(climber)
        self.draw_climbers()

    def draw_climbers(self):
        for i, climber in enumerate(self.climber_list):
            self.surf_climbers.blit(climber.surf, (50 + int(i/4), 18*(i%4)))
        self.surf.blit(self.surf_climbers, (0,0))

    def highlight(self):
        if self._highlighted:
            pg.draw.circle(self.surf, (10,10,10), (self.radius, self.radius), self.radius, 4)
        else:
            pg.draw.circle(self.surf, (255,255,255), (self.radius, self.radius), self.radius, 4)
        #self.draw_climbers()

    def set(self, attr, value):
        if attr == 'highlighted':
            self._highlighted = value
            self.highlight()
        else:
            print(f"Attribute {attr} of {self.__class__} does not support the 'set' method")


    def process_kwargs(self,kwargs):
        """Various optional customization you can change by passing kwargs."""
        settings = {
            "altitude"      : 0,
            "move_cost"     : 1,
            "accl_cost"     : 0,
            "VP"            : 1,
            "pos"           : (0, 0),
            "start_node"    : False,
            "adjacent"      : []
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(self.__class__.__name__, kwarg))
        self.__dict__.update(settings)

class WeightedGraph:
    def __init__(self, nodes=None):
        self.nodes = {}
        if nodes != None:
            for nodename, val in nodes.items():
                self.add_node(nodename, **val)
            
            # now for adjacent nodes (need to initialize all nodes first so we can reference the (previously) non-existent ones
            edge_weight = 1
            for nodename, node in self.nodes.items():
                for adj in node.adjacent:
                    self.add_edge(nodename, adj, edge_weight)
    
    def add_node(self, nodename, **kwargs):
        self.nodes[nodename] = Node(nodename, **kwargs)
        if 'start_node' in kwargs and kwargs['start_node']:
            self.start_node = self.nodes[nodename]

    def add_edge(self, nodename1, nodename2, weight):
        if not self.nodes[nodename1].neighbors.__contains__(nodename2):
            self.nodes[nodename1].neighbors[nodename2] = weight
            self.nodes[nodename2].neighbors[nodename1] = weight
    
    def find_path(self, start, target):
        if start not in self.nodes:
            print(f"ERROR! Node '{start}' is not in the provided graph!")
            return None
        if target not in self.nodes:
            print(f"ERROR! Node '{target}' is not in the provided graph!")
            return None

        dist, prev = self.dijkstra(start)
        path = [target]
        while True:
            p = prev[path[-1]]
            path.append(p)
            if p == start:
                break

        path.reverse()
        return path, dist[target]

    def dijkstra(self, start, edges=False):
        if start not in self.nodes:
            print(f"ERROR! Node '{start}' is not in the provided graph!")
            return None
        Q = {}
        dist = {}
        prev = {}
        for key, node in self.nodes.items():
            dist[key] = 1000000
            prev[key] = -1
            Q[key] = dist[key]
        dist[start] = 0
        
        while len(Q) > 0:
            u = min(Q, key=Q.get)
            del Q[u]

            for v in self.nodes[u].neighbors:
                # if move cost is in edges (first), or if the nodes are weighted (latter)
                if edges:
                    alt = dist[u] + self.nodes[u].neighbors[v]
                else:
                    alt = dist[u] + self.nodes[v].move_cost + self.nodes[v].weather_penalty['move']
                if alt < dist[v]:
                    dist[v] = alt
                    Q[v] = alt
                    prev[v] = u

        return dist, prev
