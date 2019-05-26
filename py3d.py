from typing import Tuple

from PIL import Image, ImageDraw

Point3D = Tuple[float, float, float]
Point = Tuple[float, float]


def project(C: Point3D, P: Point3D, A: Point3D, B: Point3D, D: Point3D) -> Point:
    W = [b - a for a, b in zip(A, B)]
    H = [b - a for a, b in zip(B, D)]
    K = [-(b - a) for a, b in zip(P, C)]
    F = [b - a for a, b in zip(A, C)]

    #   K*s + W*t + H*u  = F      #
    # +-                       -+ #
    # | K[0]  W[0]  H[0]   F[0] | #
    # | K[1]  W[1]  H[1]   F[1] | #
    # | K[2]  W[2]  H[2]   F[2] | #
    # +-                       -+ #

    print(K, W, H, F)

    a = (K[2] * W[0] - K[0] * W[2]) * (K[1] * F[0] - K[0] * F[1])
    a -= (K[1] * W[0] - K[0] * W[1]) * (K[2] * F[0] - K[0] * F[2])
    b = (K[2] * W[0] - K[0] * W[2]) * (K[1] * H[0] - K[0] * H[1])
    b -= (K[1] * W[0] - K[0] * W[1]) * (K[2] * H[0] - K[0] * H[2])
    u = a / b
    t = (K[1] * F[0] - K[0] * F[1] - u * (K[1] * H[0] - K[0] * H[1])) / (K[1] * W[0] - K[0] * W[1])

    w = sum(x ** 2 for x in W) ** .5
    h = sum(x ** 2 for x in H) ** .5

    o = t * w, u * h
    print(o)
    return o


WID, HEI = 100, 100
image = Image.new("RGBA", (WID, HEI))
draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, WID, HEI), fill=(255, 255, 255))

black = (0, 0, 0)

camera = (0, 0, 0)
A = (-WID/2, HEI/2, 100)
B = (WID/2, HEI/2, 100)
D = (WID/2, -HEI/2, 100)

for i in range(2):
    for j in range(2):
        for k in range(2):
            P = (20*i-10, 20*j-10, 20*k+40)
            x, y = project(camera, P, A, B, D)
            draw.point((x, y), fill=black)


image.save("output.png")
