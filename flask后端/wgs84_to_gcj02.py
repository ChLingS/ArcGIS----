from __future__ import division
from math import pi,sqrt,sin,cos
from shapely.geometry import Polygon, MultiPolygon
from pyproj import Transformer
# a python binding of https://on4wp7.codeplex.com/SourceControl/changeset/view/21483#353936

# Krasovsky 1940
#
# a = 6378245.0, 1/f = 298.3
# b = a * (1 - f)
# ee = (a^2 - b^2) / a^2
a = 6378245.0
ee = 0.00669342162296594323

# World Geodetic System ==> Mars Geodetic System
def transform_wgs84_gcj02(wgLat, wgLon):
    """
    transform(latitude,longitude) , WGS84
    return (latitude,longitude) , GCJ02
    """
    if outOfChina(wgLat, wgLon):
        mgLat = wgLat
        mgLon = wgLon
    else:
        dLat = transformLat(wgLon - 105.0, wgLat - 35.0)
        dLon = transformLon(wgLon - 105.0, wgLat - 35.0)
        radLat = wgLat / 180.0 * pi
        magic = sin(radLat)
        magic = 1 - ee * magic * magic
        sqrtMagic = sqrt(magic)
        dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
        dLon = (dLon * 180.0) / (a / sqrtMagic * cos(radLat) * pi)
        mgLat = wgLat + dLat
        mgLon = wgLon + dLon
    return mgLat, mgLon

def outOfChina(lat, lon):
    if (lon < 72.004 or lon > 137.8347):
        return True
    if (lat < 0.8293 or lat > 55.8271):
        return True
    return False

def transformLat(x, y):
    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(y * pi) + 40.0 * sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * sin(y / 12.0 * pi) + 320 * sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret

def transformLon(x, y):
    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x))
    ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * sin(x * pi) + 40.0 * sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * sin(x / 12.0 * pi) + 300.0 * sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret


def toMultiPolygon(polygon: MultiPolygon) -> MultiPolygon:
    new_polygons = []
    for polygon_part in polygon:
        new_polygon_part = []
        for wgLon, wgLat in polygon_part.exterior.coords:
            new_wgLat, new_wgLon = transform_wgs84_gcj02(wgLat, wgLon)
            new_polygon_part.append((new_wgLon, new_wgLat))
        new_polygons.append(Polygon(new_polygon_part))  # 创建新的 Polygon 对象
    # 创建新的 MultiPolygon 对象
    new_multi_polygon = MultiPolygon(new_polygons)
    return new_multi_polygon


def transformTocrs(utm_x, utm_y):
    # 初始化坐标参考系统
    crs_utm = "EPSG:32650"  # UTM zone 50N
    crs_wgs84 = "EPSG:4326"  # WGS84

    # 创建坐标转换器
    transformer = Transformer.from_crs(crs_utm, crs_wgs84)
    # 转换为 WGS84 坐标
    lat, lon = transformer.transform(utm_x, utm_y)
    return lat, lon


def toMultiPolygonGCJ(polygon: MultiPolygon) -> MultiPolygon:
    new_polygons = []
    for polygon_part in polygon:
        new_polygon_part = []
        for wgLon, wgLat in polygon_part.exterior.coords:
            new_wgLat, new_wgLon = transformTocrs(wgLat, wgLon)
            new_polygon_part.append((new_wgLon, new_wgLat))
        new_polygons.append(Polygon(new_polygon_part))  # 创建新的 Polygon 对象
    # 创建新的 MultiPolygon 对象
    new_multi_polygon = MultiPolygon(new_polygons)
    return new_multi_polygon
