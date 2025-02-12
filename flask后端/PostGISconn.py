import psycopg2
import geojson
import json
from ToolBox.wgs84_to_gcj02 import toMultiPolygon, toMultiPolygonGCJ
from shapely import wkb
from shapely.wkb import loads
from shapely.geometry import shape, mapping, Point, Polygon, MultiPolygon



db_config = {
    "host" : "localhost",
    "database" : "fuzhou",
    "user" : "postgres",
    "password" : "nm3231660"
}

def TestPost() -> None:
    connection = psycopg2.connect(**db_config)

    cursor = connection.cursor()

    # 执行 SQL 查询
    cursor.execute("SELECT Find_SRID('fuzhou', '抚州', 'geom');")

    # 获取查询结果
    db_version = cursor.fetchone()
    print("PostgreSQL 数据库版本:", db_version)

    # 关闭连接
    cursor.close()
    connection.close()

def SearchInCunPostGIS(table: str, colum: str, cun: str):
    # 连接到 PostgreSQL 数据库
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    # 执行 SQL 查询
    cursor.execute(f"SELECT gid, shi_12, xian_12, zhen_12, cun, statuses, message,ST_AsBinary(ST_Transform({colum}, 4326)) FROM {table} WHERE cun = '{cun}';")
    # 获取所有结果
    results = cursor.fetchall()
    geojson_list = []
    for row in results:
        geom = wkb.loads(bytes(row[7]))  # 将字符串转换为字节对象
        # print(geom)
        trans_geom = toMultiPolygon(geom)
        feature = geojson.Feature(geometry=trans_geom)
        feature['properties']['id'] = row[0]  # 添加 id 到 properties
        feature['properties']['shi_12'] = row[1]  # 添加 shi_12 到 properties
        feature['properties']['xian_12'] = row[2]  # 添加 xian_12 到 properties
        feature['properties']['zhen_12'] = row[3]  # 添加 zhen_12 到 properties
        feature['properties']['cun'] = row[4]  # 添加 cun 到 properties
        feature['properties']['statuses'] = row[5]  # 添加 cun_12 到 properties
        feature['properties']['message'] = row[6]  # 添加 cun_12 到 properties
        geojson_list.append(feature)
    # 创建一个 FeatureCollection
    feature_collection = geojson.FeatureCollection(geojson_list)

    # 关闭连接
    cursor.close()
    connection.close()

    # 返回 GeoJSON
    return json.dumps(feature_collection)


def create_geojson(row):
    # 解析字段
    feature_id, decimal_value, *other_fields = row

    # 创建 Geometry
    wkb_geometry = other_fields[-1]  # 假设最后一个字段是 WKB 格式的几何信息
    # print(wkb_geometry)

    geometry = loads(wkb_geometry, hex=True)
    
    new_geometry = toMultiPolygon(geometry)
    # print(new_geometry)
    # print("feature_id",feature_id)
    # print("decimal_value",decimal_value)
    # print("other_fields",other_fields)
    # 创建 Properties
    properties = {
        'id': feature_id, 
        'shi_12': other_fields[0],
        'xian_12': other_fields[1],
        'zhen_12': other_fields[2],
        'cun':other_fields[3],
        'statuses':other_fields[4],
        'message':other_fields[5],
    }

    # 创建 Feature 对象
    feature = geojson.Feature(geometry=new_geometry, properties=properties)
    return feature



def SearchPointInPostGIS(table: str, point: str, distance: float):
    # 连接到 PostgreSQL 数据库
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    # 执行 SQL 查询
    cursor.execute(f"""
        SELECT gid, sheng_12, shi_12, xian_12, zhen_12, cun, statuses, message, geom FROM {table}
        WHERE ST_DWithin(
            utm_geom,
            ST_Transform(ST_GeomFromText('POINT({point})', 4326), 32650),
            {distance}
        );
    """)
    # 获取所有结果
    results = cursor.fetchall()
    # print(results)
    geojson_list = []
    for row in results:
        # print(row)
        geojson_list.append( create_geojson(row) )
        # break
    # 创建一个 FeatureCollection
    feature_collection = geojson.FeatureCollection(geojson_list)
    # print(feature_collection)
    # 关闭连接
    cursor.close()
    connection.close()
    return json.dumps(feature_collection)


def get_unique_values(table: str, column: str):
    # 连接到 PostgreSQL 数据库
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    # 执行 SQL 查询
    cursor.execute(f"SELECT DISTINCT {column} FROM {table};")

    # 获取所有结果
    results = cursor.fetchall()

    # 关闭连接
    cursor.close()
    connection.close()

    # 返回唯一值
    return [row[0] for row in results]

def get_condition_unique_values(table: str, column: str, condition_column: str, condition_value: str):
    # 连接到 PostgreSQL 数据库
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    # 执行 SQL 查询
    cursor.execute(f"""
        SELECT DISTINCT {column} FROM {table}
        WHERE {condition_column} = '{condition_value}';
    """)

    # 获取所有结果
    results = cursor.fetchall()

    # 关闭连接
    cursor.close()
    connection.close()

    # 返回唯一值
    return [row[0] for row in results]

def get_rid_toChange_statuses(shi: str, rid: int, change_type: int) -> None:
    # 连接到 PostgreSQL 数据库
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(f"""
        UPDATE "public"."{shi}" SET "statuses" = {change_type} WHERE "gid" = {rid};
    """)
    connection.commit()
    cursor.close()
    connection.close()

def get_rid_toChange_message(shi: str, rid: int, change_message: str) -> None:
    # 连接到 PostgreSQL 数据库
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(f"""
        UPDATE "public"."{shi}" SET "message" = '{change_message}' WHERE "gid" = {rid};
    """)
    connection.commit()
    cursor.close()
    connection.close()


def delete_area(shi: str):
    # 连接到 PostgreSQL 数据库
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute(f"""
        DELETE FROM "public"."{shi}" WHERE "statuses" = 3;
    """)
    connection.commit()
    cursor.close()
    connection.close()

    
    

if __name__ == "__main__":
    # res = SearchInPostGIS(
    #         table='抚州剔除白莲后_添加村_第二版',
    #         colum='geom',
    #         cun='塘背村委会'
    #         )
    res = SearchPointInPostGIS('抚州', '116.1849269 26.85455', 1000)
    print(res)
    # res = get_unique_values('抚州剔除白莲后_添加村_第二版', 'xian_12')
    # TestPost()
    # SearchInCunPostGIS('抚州剔除白莲后_添加村_第二版', 'geom', '游军村委会')
    pass