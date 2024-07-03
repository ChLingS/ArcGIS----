import arcpy
import os
from asset import Global

CUN_SHP = Global.CUN_SHP

OUT_CORS: str = r'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'


# def erase_framland(city: str, path: str) -> None:
#     arcpy.analysis.PairwiseErase(path,
#                                  r"F:\企业实习\早稻\长势边界\人保地块提取_总（改）.shp",
#                                  fr"F:\企业实习\原始地块(补全全省)\江西省{city}.shp", None)


def space_SpatialJoin(city: str) -> None:
    feature_path: str = fr"F:\企业实习\早稻\补全早稻\投影后的矢量\江西省{city}.shp"
    out_folder: str = fr"F:\企业实习\早稻\补全早稻\{city}"
    os.makedirs(out_folder, exist_ok=True)
    arcpy.analysis.SpatialJoin(feature_path, CUN_SHP,
                               fr"{out_folder}\江西省{city}.shp",
                               "JOIN_ONE_TO_ONE",
                               "KEEP_ALL",
                               'FID "FID" true true false 255 Text 0 0,First,'
                               f'#,{feature_path},FID,-1,-1;sheng "sheng" true true false 40 Text 0 0,First,'
                               f'#,{CUN_SHP},sheng,0,40;shi "shi" true true false 40 Text 0 0,First,'
                               f'#,{CUN_SHP},shi,0,40;xian "xian" true true false 40 Text 0 0,First,'
                               f'#,{CUN_SHP},xian,0,40;zhen "zhen" true true false 40 Text 0 0,First,'
                               f'#,{CUN_SHP},zhen,0,40;cun "cun" true true false 40 Text 0 0,First,'
                               f'#,{CUN_SHP},cun,0,40;shi_code "shi_code" true true false 50 Text 0 0,First,'
                               f'#,{CUN_SHP},shi_code,0,50;xian_code "xian_code" true true false 50 Text 0 0,First,'
                               f'#,{CUN_SHP},xian_code,0,50;zhen_code "zhen_code" true true false 50 Text 0 0,First,'
                               f'#,{CUN_SHP},zhen_code,0,50;cun_code "cun_code" true true false 50 Text 0 0,First,'
                               f'#,{CUN_SHP},cun_code,0,50;sheng_code "sheng_code" true true false 50 Text 0 0,First,'
                               f'#,{CUN_SHP},sheng_code,0,50',
                               "LARGEST_OVERLAP", None, '')


def connect_cun_zonal_ZD(shp_folder_path: str, city: str, tif: str, database: str, del_mid_file: bool) -> str:
    shp_path: str = fr"{shp_folder_path}\江西省{city}.shp"
    out_feature: str = fr"{shp_folder_path}\连接\江西省{city}.shp"
    os.makedirs(f"{shp_folder_path}\连接", exist_ok=True)
    if os.path.exists(out_feature):
        return out_feature
    if not os.path.exists(shp_path):
        raise FileNotFoundError(f"{shp_path} does not exist.")
    if not os.path.exists(database):
        raise FileNotFoundError(f"{database} does not exist.")

        # return ""
    # print(out_feature)
    arcpy.analysis.SpatialJoin(shp_path, CUN_SHP,
                               f"{out_feature}",
                               "JOIN_ONE_TO_ONE",
                               "KEEP_ALL",
                               'FID "FID" true true false 255 Text 0 0,First,'
                               f'#,{shp_path},FID,-1,-1;sheng "sheng" true true false 40 Text 0 0,First,'
                               f'#,{CUN_SHP},sheng,0,40;shi "shi" true true false 40 Text 0 0,First,'
                               f'#,{CUN_SHP},shi,0,40;xian "xian" true true false 40 Text 0 0,First,'
                               f'#,{CUN_SHP},xian,0,40;zhen "zhen" true true false 40 Text 0 0,First,'
                               f'#,{CUN_SHP},zhen,0,40;cun "cun" true true false 40 Text 0 0,First,'
                               f'#,{CUN_SHP},cun,0,40;shi_code "shi_code" true true false 50 Text 0 0,First,'
                               f'#,{CUN_SHP},shi_code,0,50;xian_code "xian_code" true true false 50 Text 0 0,First,'
                               f'#,{CUN_SHP},xian_code,0,50;zhen_code "zhen_code" true true false 50 Text 0 0,First,'
                               f'#,{CUN_SHP},zhen_code,0,50;cun_code "cun_code" true true false 50 Text 0 0,First,'
                               f'#,{CUN_SHP},cun_code,0,50;sheng_code "sheng_code" true true false 50 Text 0 0,First,'
                               f'#,{CUN_SHP},sheng_code,0,50',
                               "LARGEST_OVERLAP", None, '')

    out_table: str = f"{database}\\{city}_tj2"
    table = arcpy.sa.ZonalStatisticsAsTable(out_feature, "FID",
                                            tif,
                                            out_table, "DATA", "SUM",
                                            "CURRENT_SLICE", 90, "AUTO_DETECT", "ARITHMETIC", 360)

    print(f"\r{city}正在连接字段")
    arcpy.management.JoinField(out_feature, "FID",
                               out_table, "FID",
                               "SUM", "NOT_USE_FM", None)
    arcpy.management.CalculateGeometryAttributes(out_feature, "mianji AREA", '', "SQUARE_METERS",
                                                 'PROJCS["WGS_1984_UTM_Zone_50N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",117.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
                                                 "SAME_AS_INPUT")
    if del_mid_file:
        arcpy.Delete_management(out_table)
    return out_feature


def CalculateField(shp: str, city: str, thresholds: str, out_folder: str, del_mid_file: bool) -> None:
    # 计算字段
    print(f"{city}开始")
    # shp: str = fr"F:\企业实习\早稻\补全早稻\投影后的矢量\江西省{city}.shp"
    out_shp: str = fr"{out_folder}\江西省{city}.shp"
    fields: list[str] = [f.name for f in arcpy.ListFields(shp)]
    print(fields)
    if 'mianji' not in fields and "SUM" not in fields:
        raise ValueError(f"{shp}\n字段错误!")
    if not os.path.exists(out_shp):
        fields: list[str] = [f.name for f in arcpy.ListFields(shp)]
        field_name: str = "zd"
        if field_name not in fields:
            field_type: str = "DOUBLE"
            arcpy.AddField_management(shp, field_name, field_type)
            # 计算面积占比
            expression = "!SUM! * 100 / !mianji!"
            arcpy.CalculateField_management(shp, field_name, expression, "PYTHON_9.3")
        # 创建要素图层
        print(f"\r{city}创建要素图层")
        feature_layer: str = "FeatureLayer"
        arcpy.MakeFeatureLayer_management(shp, feature_layer)

        # 按属性选择字段 "ych" 下值大于 0.2 的要素
        print(f"\r{city}筛选字段")
        query = f'"{field_name}" > {thresholds}'
        arcpy.SelectLayerByAttribute_management(feature_layer, "NEW_SELECTION", query)
        arcpy.CopyFeatures_management(feature_layer, out_shp)
        # 保存所选要素到新的 shapefile 文件
        print(f"\r{city}保存")
        arcpy.Delete_management(feature_layer)
        if del_mid_file:
            arcpy.Delete_management(shp)


def Zone(city: list[str], shp_path: str, tif_path: str, thresholds: str, database: str, out_folder: str, del_mid_file: bool):
    for city in city:
        path_after_connect = connect_cun_zonal_ZD(
            shp_folder_path=shp_path, city=city, tif=tif_path, database=database, del_mid_file=del_mid_file)
        CalculateField(
            shp=path_after_connect, city=city, thresholds=thresholds, out_folder=out_folder, del_mid_file=del_mid_file)


if __name__ == '__main__':
    res = Global.get_shpfiles_from_folder(r'F:\企业实习\原始地块（全省）\江西省耕地地块数据')
    # print(res)

    # with multiprocessing.Pool(11) as pool:
    #     pool.map(
    #         CalculateField, Global.jiangxi_cities
    #     )

    # path, city_name = '', ''
    # city_path: list[str] = []
    # for i in range(0, len(res)):
    #     # print(Global.jiangxi_cities[i])
    #     for city in Global.jiangxi_cities:
    #         if city[:-1] in res[i]:
    #             city_name = city
    #             path = res[i]
    #             # city_path.append(path)
    #             break
    #     print(city_name)
    #     print(path)

    #     erase_framland(city_name, path)
    # connect_cun_zonal_ZD
    for i in Global.jiangxi_cities:
        CalculateField(i)
        space_SpatialJoin(i)
