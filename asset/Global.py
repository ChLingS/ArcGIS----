import os
import arcpy
import pandas as pd


CUN_SHP = r"F:\企业实习\早稻\长势数据提交\江西村边界.shp"

jiangxi_cities: list[str] = ["南昌市", "九江市", "上饶市", "抚州市", "宜春市", "吉安市", "赣州市", "景德镇市",
                             "萍乡市",
                             "新余市", "鹰潭市"]


def get_shpfiles_from_folder(folder_path: str) -> list[str]:
    # 获取当前文件夹下所有的shp文件
    shp_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.shp'):
                shp_files.append(os.path.join(root, file))
    return shp_files


def get_shpfiles_from_all_folder(folder_path: str) -> list[str]:
    # 获取文件夹中所有的shp文件
    return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.shp')]


def DataRead(features: str) -> pd.DataFrame:
    """
    Read specified fields from a feature class and return the data as a DataFrame.

    Args:
        features (str): The path to the feature class.

    Returns:
        pd.DataFrame: A DataFrame containing the specified fields' data.
    @Author:
        LishuChang
    """
    # 读取字段名
    fields: list[str] = [f.name for f in arcpy.ListFields(features)]
    # 根据字段名读取数据
    data: list[dict] = [row for row in arcpy.da.SearchCursor(features, fields)]
    df: pd.DataFrame = pd.DataFrame(data, columns=fields)
    return df
