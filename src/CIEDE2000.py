import math


def rgb2xyz(rgb):
    new_rgb = []
    for v in rgb:
        c = v / 255.
        if c > 0.04045:
            c = ((c + 0.055) / 1.055) ** 2.4
        else:
            c = c / 12.92
        new_rgb.append(c * 100)
    rgb = new_rgb
    xyz = [0., 0., 0.]
    xyz[0] = rgb[0] * 0.4124 + rgb[1] * 0.3576 + rgb[2] * 0.1805
    xyz[1] = rgb[0] * 0.2126 + rgb[1] * 0.7152 + rgb[2] * 0.0722
    xyz[2] = rgb[0] * 0.0193 + rgb[1] * 0.1192 + rgb[2] * 0.9505
    return xyz



def xyz2lab(xyz):
    xyz[0] = xyz[0] / 95.047
    xyz[1] = xyz[1] / 100.00
    xyz[2] = xyz[2] / 108.883
    new_xyz = []
    for v in xyz:
        if v > 0.008856:
            c = v ** (1. / 3.)
        else:
            c = (7.787 * v) + (16. / 116.)
        new_xyz.append(c)
    xyz = new_xyz
    lab = [0., 0., 0.]
    lab[0] = (116. * xyz[1]) - 16.
    lab[1] = 500. * (xyz[0] - xyz[1])
    lab[2] = 200. * (xyz[1] - xyz[2])
    return lab


# Converts RGB pixel array into LAB format.
#
def rgb2lab(rgb):
    return xyz2lab(rgb2xyz(rgb))


def degrees(n):
    return n * (180. / math.pi)


def radians(n):
    return n * (math.pi / 180.)


def hpf(x, y):
    if x == 0 and y == 0:
        return 0
    else:
        tmphp = degrees(math.atan2(x, y))
        if tmphp >= 0:
            return tmphp
        else:
            return tmphp + 360.


def dhpf(c1, c2, h1p, h2p):
    if c1 * c2 == 0:
        return 0
    elif abs(h2p - h1p) <= 180:
        return h2p - h1p
    elif h2p - h1p > 180:
        return (h2p - h1p) - 360.
    elif h2p - h1p < 180:
        return (h2p - h1p) + 360.
    else:
        return None


def ahpf(c1, c2, h1p, h2p):
    if c1 * c2 == 0:
        return h1p + h2p
    elif abs(h1p - h2p) <= 180:
        return (h1p + h2p) / 2.
    elif abs(h1p - h2p) > 180 and h1p + h2p < 360:
        return (h1p + h2p + 360.) / 2.
    elif abs(h1p - h2p) > 180 and h1p + h2p >= 360:
        return (h1p + h2p - 360.) / 2.
    return None


def ciede2000(lab1, lab2):
    L1 = lab1[0]
    A1 = lab1[1]
    B1 = lab1[2]
    L2 = lab2[0]
    A2 = lab2[1]
    B2 = lab2[2]
    kL = 1
    kC = 1
    kH = 1
    C1 = math.sqrt((A1 ** 2.) + (B1 ** 2.))
    C2 = math.sqrt((A2 ** 2.) + (B2 ** 2.))
    aC1C2 = (C1 + C2) / 2.
    G = 0.5 * (1. - math.sqrt((aC1C2 ** 7.) / ((aC1C2 ** 7.) + (25. ** 7.))))
    a1P = (1. + G) * A1
    a2P = (1. + G) * A2
    c1P = math.sqrt((a1P ** 2.) + (B1 ** 2.))
    c2P = math.sqrt((a2P ** 2.) + (B2 ** 2.))
    h1P = hpf(B1, a1P)
    h2P = hpf(B2, a2P)
    dLP = L2 - L1
    dCP = c2P - c1P
    dhP = dhpf(C1, C2, h1P, h2P)
    dHP = 2. * math.sqrt(c1P * c2P) * math.sin(radians(dhP) / 2.)
    aL = (L1 + L2) / 2.
    aCP = (c1P + c2P) / 2.
    aHP = ahpf(C1, C2, h1P, h2P)
    T = 1. - 0.17 * math.cos(radians(aHP - 39)) + 0.24 * math.cos(radians(2. * aHP)) + 0.32 * math.cos(
        radians(3. * aHP + 6.)) - 0.2 * math.cos(radians(4. * aHP - 63.))
    dRO = 30. * math.exp(-1. * (((aHP - 275.) / 25.) ** 2.))
    rC = math.sqrt((aCP ** 7.) / ((aCP ** 7.) + (25. ** 7.)))
    sL = 1. + ((0.015 * ((aL - 50.) ** 2.)) / math.sqrt(20. + ((aL - 50.) ** 2.)))
    sC = 1. + 0.045 * aCP
    sH = 1. + 0.015 * aCP * T
    rT = -2. * rC * math.sin(radians(2. * dRO))
    return ((dLP / (sL * kL)) ** 2.) + ((dCP / (sC * kC)) ** 2.) + ((dHP / (sH * kH)) ** 2.) + rT * (
            dCP / (sC * kC)) * (
                   dHP / (sH * kH))

