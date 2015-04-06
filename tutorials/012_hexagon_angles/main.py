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
    INSIDE_ANGLE_DEG = 60

    _base_angle_deg = 30

    @classmethod
    def set_base_angle_deg(cls, deg):
        cls._base_angle_deg = deg

    @classmethod
    def get_corner_angle_deg(cls, i):
        return cls._base_angle_deg + cls.INSIDE_ANGLE_DEG * i

    @classmethod
    def get_corner_angle_rad(cls, i):
        return pi / 180 * cls.get_corner_angle_deg(i)
        
    @classmethod
    def create_corner_position(cls, center, size, i):
        angle_rad = cls.get_corner_angle_rad(i)
        return Position(
                center.x + size * cos(angle_rad), 
                center.y + size * sin(angle_rad))

    @classmethod
    def create_corner_vertex(cls, center, size, i):
        angle_rad = cls.get_corner_angle_rad(i)
        cos_angle_rad = cos(angle_rad)
        sin_angle_rad = sin(angle_rad)
        return Vertex(
                center.x + size * cos_angle_rad, 
                center.y + size * sin_angle_rad,
                cos_angle_rad, 
                sin_angle_rad)

    @classmethod
    def create_corner_angles(cls):
        return [cls.get_corner_angle_deg(i) for i in xrange(6)]

    @classmethod
    def create_corner_positions(cls, center, edge_len):
        return [cls.create_corner_position(center, edge_len, i) for i in xrange(6)]

    @classmethod
    def create_corner_vertices(cls, center, edge_len):
        return [cls.create_corner_vertex(center, edge_len, i) for i in xrange(6)]


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
        self.make_corner_labels()

        self.inner_angle_label = Label(text=u"{0}°".format(Hexagon.INSIDE_ANGLE_DEG), pos_hint={}, size_hint=(None, None))
        self.add_widget(self.inner_angle_label)

    def make_corner_labels(self):
        corner_angle_degs = Hexagon.create_corner_angles()
        corner_labels = [Label(text=u"{0}°".format(e), pos_hint={}, size_hint=(None, None)) for e in corner_angle_degs]
        for corner_label in corner_labels:
            self.add_widget(corner_label)

        self.corner_labels = corner_labels

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

            Line(points=KivyHexagon.convert_line_points([corner_positions[0], center_position, corner_positions[-1]]))

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

        self.inner_angle_label.center = (center_position.x + 30, center_position.y)

class HexagonApp(App):
    pass

if __name__ == '__main__':
    HexagonApp().run()
