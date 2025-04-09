import math
import numpy as np
from pyproj import Transformer


def LBH2XYZ(L: float, B: float, H: float, coorSys: str):
    """
    经纬高转地心XYZ（X指向0°经线与协议赤道焦点，Z指向协议北极，Y轴与X、Z成右手正交，由Z到X大拇指指向方向为Y）
    :param L: 经度,单位°
    :param B: 纬度（地理纬度），单位°
    :param H: 高度，单位m
    :param coorSys 坐标系选择，参数可以为"wgs84"、"cgcs2000"，
    两种坐标系所采取的椭圆半长轴均为6378137m，扁率不同，
    wgs84的扁率为1/298.257223564，半短轴为6356752.314245251，偏心率e为0.08181919084248535
    cgcs2000的扁率为1/298.257222101，半短轴为6356752.314140356，偏心率e为0.08181919104281517
    :return: 地心XYZ 单位m
    """
    L = L / 180 * math.pi  # 先转为弧度
    B = B / 180 * math.pi  # 先转为弧度

    a = 6378137  # 半长轴
    if coorSys == "wgs84":
        e = 0.08181919084248535
    elif coorSys == "cgcs2000":
        e = 0.08181919104281517
    N = a / math.sqrt(1 - math.pow(e, 2) * math.pow(math.sin(B), 2))

    X = (N + H) * math.cos(B) * math.cos(L)
    Y = (N + H) * math.cos(B) * math.sin(L)
    Z = (N * (1 - math.pow(e, 2)) + H) * math.sin(B)

    return X, Y, Z


def XYZ2LBH(X: float, Y: float, Z: float, coorSys: str):
    """
    地心非惯性坐标系（地固系）XYZ转换为L（经度）B（纬度）H（高程）
    :param X: X轴刻度值，单位m。指向0°经线与协议赤道焦点
    :param Y: Y轴刻度值，单位m。Y轴与X、Z成右手正交，由Z到X大拇指指向方向为Y
    :param Z: Z轴刻度值，单位m。指向协议北极
    :param coorSys: 坐标系选择，参数可以为"wgs84"、"cgcs2000"，
    :return: LBH  单位°、m
    """
    a = 6378137  # 半长轴
    if coorSys == "wgs84":
        e = 0.08181919084248535
    elif coorSys == "cgcs2000":
        e = 0.08181919104281517

    L = math.atan2(Y, X) / math.pi * 180

    tB = 0
    N = a / math.sqrt(1 - math.pow(e, 2) * math.pow(math.sin(tB), 2))
    B = math.atan2((Z + N * math.pow(e, 2) * math.sin(tB)), math.sqrt(X * X + Y * Y))
    while math.fabs(B - tB) > 1e-16:  # 超越方程迭代计算
        tB = B
        N = a / math.sqrt(1 - math.pow(e, 2) * math.pow(math.sin(tB), 2))
        B = math.atan2((Z + N * math.pow(e, 2) * math.sin(tB)), math.sqrt(X * X + Y * Y))

    N = a / math.sqrt(1 - math.pow(e, 2) * math.pow(math.sin(B), 2))
    if B == 0:  # 防止赤道上目标刚好为纬度0°时，无法计算的问题
        H = math.sqrt(X * X + Y * Y) / math.cos(B) - N
    else:
        H = Z / math.sin(B) - N * (1 - e * e)

    B = B / math.pi * 180
    return L, B, H


if __name__ == '__main__':
    # coords = XYZ2LBH(*LBH2XYZ(121, 31, 0, 'wgs84'), 'cgcs2000')
    # print(coords)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:4490", always_xy=True)
    print(transformer.transform(121, 31))

