Hexagon Angles
==============

헥사곤 각도

<http://www.redblobgames.com/grids/hexagons/#basics>

<p><img src="./screenshots/result.png" width=50%"/></p>

* 표준 육각형 내각(interior angle): 120 도
* 조각(wedge) 모양: 정삼각형(equilateral triangle)
* 조각 내각: 정삼각형 내각(60도)
* 조각 개수: 6 조각
* 대표 방향(typical orientation) 각도
    * 뾰족한 위(pointy topped): 30 도
    * 평평한 위(flat topped): 0 도
* i 번째 꼭지점 각도 위치: 대표 방향 각도 + (60 * i) 도


   ```python
    class Hexagon(object):
        WEDGE_ANGLE_DEG = 60

        _base_orientation_angle_deg = 30

        @classmethod
        def get_corner_angle_deg(cls, i):
            return cls._base_orientation_angle_deg + cls.INSIDE_ANGLE_DEG * i
   ```
