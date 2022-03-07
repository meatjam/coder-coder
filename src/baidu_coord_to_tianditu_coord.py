import math
PI = 3.1415926535897932384626
X_PI = PI * 3000.0 / 180.0


def baidu_coord_to_tianditu_coord(point):
    """
        :param point: 百度API返回的坐标点({'lng': 108.28813023052102,'lat': 40.897398809151599})
        :type point:dict
        :return: 转换后的天地图坐标点   ({'lng': 108.27629438610634, 'lat': 40.89016818613019})
        :rtype:dict
    """
    mars_point = baiduTomars(point)
    return transformGCJ2WGS(mars_point['lat'], mars_point['lng'])


def baiduTomars(baidu_point):
    mars_point = {"lng": 0, "lat": 0}
    x = baidu_point["lng"] - 0.0065
    y = baidu_point["lat"] - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * X_PI)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * X_PI)
    mars_point["lng"] = z * math.cos(theta)
    mars_point["lat"] = z * math.sin(theta)
    return mars_point


def transformGCJ2WGS(gcjLat, gcjLng):
    d = delta(gcjLat, gcjLng)
    return {
        'lng': gcjLng - d["lng"],
        'lat': gcjLat - d["lat"]
    }

def delta(lat, lng):
    a = 6378245.0
    ee = 0.00669342162296594323
    dLat = transformLat(lng - 105.0, lat - 35.0)
    dLng = transformLng(lng - 105.0, lat - 35.0)
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI)
    dLng = (dLng * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI)
    return {
      'lat': dLat,
      'lng': dLng
    }

def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0
    return ret

def transformLng(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x))
    ret += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0
    return ret

def main():
    print('This module does not execute in local environment!')
    return


if __name__ == '__main__':
    main()
