Hello Hexagon
=============

<http://www.redblobgames.com/grids/hexagons/#basics>

<img src="./screenshots/hello_hexagon.png?raw=true" width=50%"/>

#### 개념

* 육각형(hexagon): 6면 다각형(6-sided polygons)
* 표준 육각형(regula hexagon): 모든 면의 모서리(edge) 길이가 동일한 육각형
* 대표 방향(typical orientation) 
    * 뽀족한 꼭대기(pointy topped): 수평(horizontal) 배치
    * 평평한 꼭대기(flat topped): 수직(vertical) 배치


#### 모서리(edges)

* 6 개 모서리 구성
* 2 개 육각형 1 개 모서리 공유


#### 꼭지점(corners)

* 6 개 꼭지점 구성
* 3 개 육각형 1개 꼭지점 공유


#### 각도(angles)

* 표준 육각형 내각(interior angle): 120 도
* 6 개 정삼각형(equilateral triangle) 6조각(wedges)
* 정삼각형 내각: 60도
* i 번째 꼭지점 각도 위치: (60 * i) + 90 도

   ```python
   class Hexagon(object):
      @classmethod
         def create_corner_position(cls, center, size, i):
            angle_deg = 60 * i + 90
            angle_rad = pi / 180 * angle_deg
            return Position(
                    center.x + size * cos(angle_rad), 
                    center.y + size * sin(angle_rad))
   ```
* 모든 꼭지점 위치 목록

   ```python
    class Hexagon(object):
        @classmethod
        def create_corner_positions(cls, center, edge_len):
            return [cls.create_corner_position(center, edge_len, corner_index) for corner_index in range(6)]
   ```
