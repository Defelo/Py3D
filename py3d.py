import math
from typing import Tuple, List

from PIL import Image, ImageDraw

import vector
from lineqsysolve import solve

FOV: float = 60

Point3D = Tuple[float, float, float]
Point = Tuple[float, float]


def raycast(source: Point3D, yaw: float, pitch: float, d: float) -> Point3D:
    yaw: float = yaw * math.pi / 180
    pitch: float = pitch * math.pi / 180

    x: float = math.cos(yaw) * d
    y: float = math.sin(pitch) * d
    z: float = math.sin(yaw) * d

    return source[0] + x, source[1] + y, source[2] + z


def project(c: Point3D, p: Point3D, yaw: float, pitch: float, roll: float) -> Point:
    a: Point3D = raycast(c, yaw + FOV / 2, pitch + FOV / 2, 100)
    b: Point3D = raycast(c, yaw - FOV / 2, pitch + FOV / 2, 100)
    d: Point3D = raycast(c, yaw - FOV / 2, pitch - FOV / 2, 100)

    # c + (p-c)*s = a + (b-a)*t + (d-b)*u
    # (c-p)*s + (b-a)*t + (d-b)*u = c-a
    matrix: List[List[float]] = []
    for i in range(3):
        row: List[float] = [
            c[i] - p[i],
            b[i] - a[i],
            d[i] - b[i],
            c[i] - a[i]
        ]
        matrix.append(row)
    _, t, u = solve(matrix)

    vec: vector.Vector = vector.Point(t - 0.5, u - 0.5).to_vector()
    vec.angle -= roll
    t, u = vec.to_point()
    return t + 0.5, u + 0.5


def cube():
    wid, hei = 100, 100
    image = Image.new("RGBA", (wid, hei))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, wid, hei), fill=(255, 255, 255))

    black = (0, 0, 0)

    draw.line((wid / 2, 0, wid / 2, hei), fill=black, width=1)
    draw.line((0, hei / 2, wid, hei / 2), fill=black, width=1)

    camera: Point3D = (0, 0, 0)

    for i in range(2):
        for j in range(2):
            for k in range(2):
                point: Point3D = (20 * i - 10, 20 * j - 10, 20 * k + 40)
                x, y = project(camera, point, 90, 0, 0)
                draw.point((x * wid, y * hei), fill=black)

    image.save("output.png")


if __name__ == '__main__':
    cube()
