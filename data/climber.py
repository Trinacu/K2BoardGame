import pygame as pg
from . import tools

class Climber():
    def __init__(self, player, graph, name):
        self.player = player
        self.graph = graph
        self.name = name
        self.color = self.player.color
        self.accl = 0

        self.radius = 8
        self.surf = pg.Surface((2*self.radius, 2*self.radius))
        self.surf.fill((255, 255, 255))
        self.surf.set_colorkey((255,255,255))
        print((*self.player.color[:3], 100))
        if self.name == 'round':
            pg.draw.circle(self.surf, self.player.color, (self.radius, self.radius), self.radius, 0)
            pg.draw.circle(self.surf, (0,0,0), (self.radius, self.radius), self.radius, 2)
        else:
            pg.draw.rect(self.surf, self.player.color, (0, 0, 2*self.radius, 2*self.radius))
            pg.draw.rect(self.surf, (0,0,0), (0, 0, 2*self.radius, 2*self.radius), 2)
        self.rect = self.surf.get_rect()

        self.accl_surf = pg.Surface((160, 30))
        self.accl_surf.fill((200,200,200))

        self.node = self.graph.start_node
        self.node.add_climber(self)

    def update_accl_surf(self):
        self.accl_surf = tools.make_text(f"Accl: {self.accl}/10", (0,0,0), (0,0), 16, fonttype='impact.ttf')[0]

    def reachable_nodes(self):
        move = 3
        move_down = 4

        dist, prev = self.graph.dijkstra(self.node.name)
        
        nodes_downwards = []
        for nodename in prev:
            if nodename == self.node.name:
                continue
            path = [nodename]
            up = False
            while True:
                p = prev[path[-1]]
                if self.graph.nodes[p].altitude < self.graph.nodes[path[-1]].altitude:
                    up = True
                    break
                path.append(p)
                if p == self.node.name:
                    break
            if not up:
                nodes_downwards.append(nodename)

        reachable = []
        for nodename, distance in dist.items():
            if distance <= move or (distance <= move_down and nodename in nodes_downwards):
                if nodename not in reachable:
                    reachable.append(nodename)

        #print(dist)
        #print(nodes_downwards)
        print(reachable)

        return reachable

