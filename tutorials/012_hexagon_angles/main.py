# -*- coding:utf8 -*-
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
            if type(args[0]) is Position:
                src = args[0]
                self.x = src.x
                self.y = src.y
            else:
                self.x, self.y = args[:2]
        else:
            self.x = kwargs['x']
            self.y = kwargs['y']

    def __repr__(self):
        return 'Position(x={0:.2f}, y={1:.2f})'.format(self.x, self.y)        

    def to_tuple(self):
        return (self.x, self.y)

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
    WEDGE_ANGLE_DEG = 60

    _base_angle_deg = 30

    @classmethod
    def set_hexagon_pointy_topped(cls):
        cls._base_angle_deg = 30

    @classmethod
    def set_hexagon_flat_topped(cls):
        cls._base_angle_deg = 0

    @classmethod
    def is_hexagon_pointy_topped(cls):
        return cls._base_angle_deg % 60 == 30

    @classmethod
    def is_hexagon_flat_topped(cls):
        return cls._base_angle_deg % 60 == 0

    @classmethod
    def get_hexagon_corner_angle_deg(cls, i):
        return cls._base_angle_deg + cls.WEDGE_ANGLE_DEG * i

    @classmethod
    def get_hexagon_corner_angle_rad(cls, i):
        return pi / 180 * cls.get_hexagon_corner_angle_deg(i)
        
    @classmethod
    def create_hexagon_corner_position(cls, center, size, i):
        angle_rad = cls.get_hexagon_corner_angle_rad(i)
        return Position(
                center.x + size * cos(angle_rad), 
                center.y + size * sin(angle_rad))

    @classmethod
    def create_hexagon_corner_vertex(cls, center, size, i):
        angle_rad = cls.get_hexagon_corner_angle_rad(i)
        cos_angle_rad = cos(angle_rad)
        sin_angle_rad = sin(angle_rad)
        return Vertex(
                center.x + size * cos_angle_rad, 
                center.y + size * sin_angle_rad,
                cos_angle_rad, 
                sin_angle_rad)

    @classmethod
    def create_hexagon_corner_angles(cls):
        return [cls.get_hexagon_corner_angle_deg(i) for i in xrange(6)]

    @classmethod
    def create_hexagon_corner_positions(cls, center, edge_len):
        return [cls.create_hexagon_corner_position(center, edge_len, i) for i in xrange(6)]

    @classmethod
    def create_hexagon_corner_vertices(cls, center, edge_len):
        return [cls.create_hexagon_corner_vertex(center, edge_len, i) for i in xrange(6)]


class KivyHexagon(Hexagon):
    @classmethod
    def gen_position_sequences(cls, positions):
        for position in positions:
            yield position.x
            yield position.y
        
    @classmethod
    def gen_closed_position_sequences(cls, positions):
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
    def convert_closed_line_points(cls, positions):
        return [e for e in cls.gen_closed_position_sequences(positions)]

    @classmethod
    def convert_mesh_vertices(cls, vertices):
        return [e for e in cls.gen_vertex_sequences(vertices)]

    @classmethod
    def make_hexagon_mesh(cls, center_position, edge_len):
        corner_vertices = cls.create_hexagon_corner_vertices(center_position, edge_len) 
        return Mesh(vertices=cls.convert_mesh_vertices(corner_vertices), indices=xrange(len(corner_vertices)), mode='triangle_fan')

    @classmethod
    def make_hexagon_outline(cls, center_position, edge_len, width=1):
        corner_positions = cls.create_hexagon_corner_positions(center_position, edge_len) 
        return Line(points=cls.convert_closed_line_points(corner_positions), width=width)

    @classmethod
    def make_circle(self, center_position, radius):
        return Ellipse(pos=(center_position.x - radius, center_position.y - radius), size=(radius * 2, radius * 2))


class HexagonRoot(FloatLayout):
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

        self.wedge_angle_label = Label(text=u"{0}°".format(Hexagon.WEDGE_ANGLE_DEG), pos_hint={}, size_hint=(None, None))
        self.add_widget(self.wedge_angle_label)

        self.corner_labels = [Label(text="", pos_hint={}, size_hint=(None, None)) for i in xrange(6)]
        for corner_label in self.corner_labels:
            self.add_widget(corner_label)

    def make_pointy_topped(self):
        KivyHexagon.set_hexagon_pointy_topped()
        self.render_canvas()

    def make_flat_topped(self):
        KivyHexagon.set_hexagon_flat_topped()
        self.render_canvas()

    def render_canvas(self, *args):
        center_position = Position(*self.center)
        corner_positions = KivyHexagon.create_hexagon_corner_positions(center_position, self.EDGE_LEN)        

        self.canvas.before.clear()

        with self.canvas.before:
            Color(*self.MESH_COLOR)
            KivyHexagon.make_hexagon_mesh(center_position, self.EDGE_LEN)

            Color(*self.EDGE_COLOR)
            KivyHexagon.make_hexagon_outline(center_position, self.EDGE_LEN)

            Line(points=KivyHexagon.convert_line_points([corner_positions[0], center_position, corner_positions[-1]]))

        corner_angle_degs = KivyHexagon.create_hexagon_corner_angles()
        for corner_label, corner_angle_deg in zip(self.corner_labels, corner_angle_degs):
            corner_label.text = u"{0}°".format(corner_angle_deg)

        for corner_label, corner_position in zip(self.corner_labels, corner_positions):
            if corner_position.x < center_position.x:
                corner_label.center = (corner_position.x - 20, corner_position.y)
            elif corner_position.x > center_position.x:
                corner_label.center = (corner_position.x + 20, corner_position.y)
            else:
                if corner_position.y < center_position.y:
                    corner_label.center = (corner_position.x, corner_position.y - 15)
                elif corner_position.y > center_position.y:
                    corner_label.center = (corner_position.x, corner_position.y + 15)

        wedge_position = KivyHexagon.create_hexagon_corner_position(center_position, self.EDGE_LEN * 0.3, 5.5)
        self.wedge_angle_label.center = wedge_position.to_tuple() 

class HexagonApp(App):
    pass

if __name__ == '__main__':
    HexagonApp().run()
