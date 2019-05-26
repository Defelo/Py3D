from typing import Tuple, List

from PIL import Image, ImageDraw

from lineqsysolve import solve

Point3D = Tuple[float, float, float]
Point = Tuple[float, float]


def project(c: Point3D, p: Point3D, a: Point3D, b: Point3D, d: Point3D) -> Point:
    # (p-c)*s + (b-a)*t + (d-b)*u = c-a
    matrix: List[List[float]] = []
    for i in range(3):
        row: List[float] = [
            p[i] - c[i],
            b[i] - a[i],
            d[i] - b[i],
            c[i] - a[i]
        ]
        matrix.append(row)
    _, t, u = solve(matrix)
    w = sum((a[i] - b[i]) ** 2 for i in range(3)) ** .5
    h = sum((b[i] - d[i]) ** 2 for i in range(3)) ** .5

    return t * w, u * h


def cube():
    wid, hei = 100, 100
    image = Image.new("RGBA", (wid, hei))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, wid, hei), fill=(255, 255, 255))

    black = (0, 0, 0)

    camera = (0, 0, 0)
    plane = [
        (-wid / 2, hei / 2, 100),
        (wid / 2, hei / 2, 100),
        (wid / 2, -hei / 2, 100)
    ]

    for i in range(2):
        for j in range(2):
            for k in range(2):
                point = (20 * i - 10, 20 * j - 10, 20 * k + 40)
                x, y = project(camera, point, *plane)
                draw.point((x, y), fill=black)

    image.save("output.png")


if __name__ == '__main__':
    cube()
