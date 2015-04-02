from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Line, Mesh
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

from math import pi, cos, sin

class Position(object):
    def __init__(self, *args, **kwargs):
        if args:
            self.x, self.y = args[:2]
        else:
            self.x = kwargs['x']
            self.y = kwargs['y']

    def __repr__(self):
        return 'Position(x={0:.2f}, y={1:.2f})'.format(self.x, self.y)        

class Vertex(object):
    def __init__(self, *args, **kwargs):
        if args:
            self.x, self.y, self.u, self.v = args[:4]
        else:
            self.x = kwargs['x']
            self.y = kwargs['y']
            self.u = kwargs['u']
            self.v = kwargs['v']

    def __repr__(self):
        return 'Vertex(x={0:.2f}, y={1:.2f}, u={2:.2f}, v={3:.2f})'.format(self.x, self.y, self.u, self.v)        


class Hexagon(object):
    @classmethod
    def create_corner_position(cls, center, size, i):
        angle_deg = 60 * i + 90
        angle_rad = pi / 180 * angle_deg
        return Position(
                center.x + size * cos(angle_rad), 
                center.y + size * sin(angle_rad))

    @classmethod
    def create_corner_vertex(cls, center, size, i):
        angle_deg = 60 * i + 90
        angle_rad = pi / 180 * angle_deg
        return Vertex(
                center.x + size * cos(angle_rad), 
                center.y + size * sin(angle_rad),
                cos(angle_rad), 
                sin(angle_rad))

    @classmethod
    def create_corner_positions(cls, center, edge_len):
        return [cls.create_corner_position(center, edge_len, corner_index) for corner_index in range(6)]

    @classmethod
    def create_corner_vertices(cls, center, edge_len):
        return [cls.create_corner_vertex(center, edge_len, corner_index) for corner_index in range(6)]


class KivyHexagon(Hexagon):
    @classmethod
    def gen_position_sequences(cls, positions):
        for position in positions:
            yield position.x
            yield position.y
        
        yield positions[0].x
        yield positions[0].y

    @classmethod
    def gen_vertex_sequences(cls, vertexs):
        for vertex in vertexs:
            yield vertex.x
            yield vertex.y
            yield vertex.u
            yield vertex.v
        
    @classmethod
    def convert_line_points(cls, positions):
        return [e for e in cls.gen_position_sequences(positions)]

    @classmethod
    def convert_mesh_vertices(cls, vertices):
        return [e for e in cls.gen_vertex_sequences(vertices)]


class HexagonRoot(FloatLayout):
    center_label = ObjectProperty()
    corner_label = ObjectProperty()
    edge_label = ObjectProperty()

    EDGE_LEN = 100
    EDGE_WIDTH = 2
    CENTER_RADIUS = 4
    CORNER_RADIUS = 4
    CENTER_COLOR = (0.5, 0.1, 0.1)
    CORNER_COLOR = (0.5, 0.1, 0.1)
    EDGE_COLOR = (0.3, 0.3, 0.3)
    MESH_COLOR = (0.5, 0.5, 0.5)

    def __init__(self, **kwargs):
        super(HexagonRoot, self).__init__(**kwargs)

        self.bind(pos=self.render_canvas, size=self.render_canvas)

    def render_canvas(self, *args):
        center_position = Position(*self.center)
        corner_positions = Hexagon.create_corner_positions(center_position, self.EDGE_LEN)        
        corner_vertices = Hexagon.create_corner_vertices(center_position, self.EDGE_LEN) 

        self.canvas.before.clear()

        with self.canvas.before:
            Color(*self.MESH_COLOR)
            Mesh(vertices=KivyHexagon.convert_mesh_vertices(corner_vertices), indices=xrange(len(corner_vertices)), mode='triangle_fan')

            Color(*self.EDGE_COLOR)
            Line(points=KivyHexagon.convert_line_points(corner_positions), width=self.EDGE_WIDTH)

            Color(*self.CENTER_COLOR)
            self.render_circle(center_position, self.CENTER_RADIUS)

            Color(*self.CORNER_COLOR)
            for corner_position in corner_positions:
                self.render_circle(corner_position, self.CORNER_RADIUS)

            Line(points=KivyHexagon.convert_line_points(corner_positions)[2*3:2*3+4], width=self.EDGE_WIDTH)

        self.center_label.center = (center_position.x, center_position.y - 20)
        self.corner_label.center = (corner_positions[2].x, corner_positions[2].y - 20)
        self.edge_label.center = (
                (corner_positions[3].x + corner_positions[4].x) / 2 + 20, 
                (corner_positions[3].y + corner_positions[4].y) / 2 - 10)


    def render_circle(self, center, radius):
        return Ellipse(pos=(center.x - radius, center.y - radius), size=(radius * 2, radius * 2))


class HexagonApp(App):
    pass

if __name__ == '__main__':
    HexagonApp().run()
