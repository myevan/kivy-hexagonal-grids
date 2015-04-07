# -*- coding:utf8 -*-
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Line, Mesh
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

from math import pi, cos, sin, sqrt

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

    @classmethod
    def get_hexagon_long_len(cls, edge_len):
        return 2 * edge_len

    @classmethod
    def get_hexagon_short_len(cls, edge_len):
        return sqrt(3.0) / 2.0 * cls.get_hexagon_long_len(edge_len)

    @classmethod
    def get_hexagon_long_step(cls, edge_len):
        return cls.get_hexagon_long_len(edge_len) / 4.0 * 3.0 

    @classmethod
    def get_hexagon_short_len(cls, edge_len):
        return sqrt(3.0) / 2.0 * cls.get_hexagon_long_len(edge_len)

    @classmethod
    def get_hexagon_short_step(cls, edge_len):
        return cls.get_hexagon_short_len(edge_len) 

    @classmethod
    def get_hexagon_size(cls, edge_len):
        if cls.is_hexagon_pointy_topped():
            return (cls.get_hexagon_short_len(edge_len), cls.get_hexagon_long_len(edge_len))
        else:
            return (cls.get_hexagon_long_len(edge_len), cls.get_hexagon_short_len(edge_len))

    @classmethod
    def get_hexagon_step(cls, edge_len):
        if cls.is_hexagon_pointy_topped():
            return (cls.get_hexagon_short_step(edge_len), cls.get_hexagon_long_step(edge_len))
        else:
            return (cls.get_hexagon_long_step(edge_len), cls.get_hexagon_short_step(edge_len))

    @classmethod
    def get_hexagon_div(cls):
        if cls.is_hexagon_pointy_topped():
            return (2, 4)
        else:
            return (4, 2)

    @classmethod
    def gen_hexagon_grid_positions(cls, origin_position, edge_len, row_count, col_count):
        size_x, size_y = cls.get_hexagon_size(edge_len)
        step_x, step_y = cls.get_hexagon_step(edge_len)

        base_position = Position(origin_position)
        base_position.x += size_x * 0.5
        base_position.y += size_y * 0.5

        line_position = Position(base_position)

        if cls._base_angle_deg == 30:
            for row in xrange(0, row_count):
                each_position = Position(line_position)
                if row % 2 == 1:
                    each_position.x += step_x * 0.5

                for col in xrange(0, col_count):
                    yield each_position
                    each_position.x += step_x 

                line_position.y += step_y 
        else:
            for col in xrange(0, col_count):
                each_position = Position(line_position)
                if col % 2 == 1:
                    each_position.y += step_y * 0.5

                for row in xrange(0, row_count):
                    yield each_position
                    each_position.y += step_y 

                line_position.x += step_x
           


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
    X_AXIS_LEN = 700
    Y_AXIS_LEN = 450

    EDGE_LEN = 100
    EDGE_WIDTH = 2
    CENTER_RADIUS = 4
    CORNER_RADIUS = 4
    CENTER_COLOR = (0.5, 0.1, 0.1)
    CORNER_COLOR = (0.5, 0.1, 0.1)
    EDGE_COLOR = (0.3, 0.3, 0.3)
    AXIS_COLOR = (0.3, 0.3, 0.3)
    MESH_COLOR = (0.5, 0.5, 0.5)

    def __init__(self, **kwargs):
        super(HexagonRoot, self).__init__(**kwargs)

        self.bind(pos=self.render_canvas, size=self.render_canvas)

    def make_pointy_topped(self):
        KivyHexagon.set_hexagon_pointy_topped()
        self.render_canvas()

    def make_flat_topped(self):
        KivyHexagon.set_hexagon_flat_topped()
        self.render_canvas()

    def render_canvas(self, *args):
        origin_position = Position(*self.center)
        origin_position.x -= self.X_AXIS_LEN / 2
        origin_position.y -= self.Y_AXIS_LEN / 2

        x_axis_position = Position(origin_position.x + self.X_AXIS_LEN, origin_position.y)
        y_axis_position = Position(origin_position.x, origin_position.y + self.Y_AXIS_LEN)

        self.canvas.before.clear()

        with self.canvas.before:
            Color(*self.AXIS_COLOR)
            Line(points=KivyHexagon.convert_line_points([x_axis_position, origin_position, y_axis_position]), width=self.EDGE_WIDTH)

            for each_position in KivyHexagon.gen_hexagon_grid_positions(origin_position, self.EDGE_LEN, row_count=2, col_count=3):
                Color(*self.MESH_COLOR)
                KivyHexagon.make_hexagon_mesh(each_position, self.EDGE_LEN)

                Color(*self.EDGE_COLOR)
                KivyHexagon.make_hexagon_outline(each_position, self.EDGE_LEN)

                Color(*self.CENTER_COLOR)
                KivyHexagon.make_circle(each_position, self.CENTER_RADIUS)

            hexagon_width, hexagon_height = KivyHexagon.get_hexagon_size(self.EDGE_LEN)
            hexagon_div_h, hexagon_div_v = KivyHexagon.get_hexagon_div()

            Color(*self.AXIS_COLOR)
            h_line_s_position = Position(origin_position)
            h_line_e_position = Position(h_line_s_position)
            h_line_e_position.x += self.X_AXIS_LEN
            for row in xrange(0, int(self.Y_AXIS_LEN / hexagon_height * hexagon_div_v)):
                Line(points=KivyHexagon.convert_line_points([h_line_s_position, h_line_e_position]))
                h_line_s_position.y += hexagon_height / hexagon_div_v
                h_line_e_position.y += hexagon_height / hexagon_div_v

            v_line_s_position = Position(origin_position)
            v_line_e_position = Position(v_line_s_position)
            v_line_e_position.y += self.Y_AXIS_LEN
            for row in xrange(0, int(self.X_AXIS_LEN / hexagon_width * hexagon_div_h)):
                Line(points=KivyHexagon.convert_line_points([v_line_s_position, v_line_e_position]))
                v_line_s_position.x += hexagon_width / hexagon_div_h
                v_line_e_position.x += hexagon_width / hexagon_div_h


class HexagonApp(App):
    pass

if __name__ == '__main__':
    HexagonApp().run()
