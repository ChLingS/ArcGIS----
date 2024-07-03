import arcpy
from arcpy import env
from arcpy.sa import *
import pandas as pd
import os
from asset.Global import DataRead, CUN_SHP

OUT_CORS: str = r'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'


class Crop_Growth:
    def __init__(self, date: str, city: str, frame_path: str, tif_file: str, out_path: str):
        self.date = date
        self.city = city
        self.frame_path = frame_path
        self.tif_file = tif_file
        self.out_path = out_path

    def get_city_orignal_tif(self):
        feature = f"{self.frame_path}/江西省{self.city}.shp"
        if not os.path.exists(feature):
            raise FileNotFoundError(f"{feature} does not exist.")
        new_raster_folder = fr"{self.out_path}/{self.city}/栅格"
        os.makedirs(new_raster_folder, exist_ok=True)
        out_raster = f"{new_raster_folder}/{self.date}{self.city}.tif"
        if os.path.exists(out_raster):
            raise FileExistsError(f"{out_raster} has been created.")
        with arcpy.EnvManager(outputCoordinateSystem=OUT_CORS):
            outExtractByMask = ExtractByMask(self.tif_file, feature, "INSIDE")
            outExtractByMask.save(out_raster)
        return out_raster

    def tif_to_shp(self):
        tif_file = self.get_city_orignal_tif()
        new_shp_folder = fr"{self.out_path}/{self.city}/矢量"
        os.makedirs(new_shp_folder, exist_ok=True)
        out_shp = f"{new_shp_folder}/{self.date}{self.city}.shp"
        if os.path.exists(out_shp):
            raise FileExistsError(f"{out_shp} has been created.")
        with arcpy.EnvManager(outputCoordinateSystem=OUT_CORS):
            arcpy.conversion.RasterToPolygon(tif_file,
                                             out_shp,
                                             "NO_SIMPLIFY", "Value",
                                             "SINGLE_OUTER_PART", None)


def Read_table(df: pd.DataFrame) -> pd.DataFrame:
    new_df = pd.DataFrame(columns=['sheng', 'sheng_code',
                                   'shi', 'shi_code',
                                   'xian', 'xian_code',
                                   'zhen', 'zhen_code',
                                   'cun', 'cun_code',
                                   '面积（亩）',
                                   'LEVEL1', 'LEVEL2', 'LEVEL3', 'LEVEL4', 'LEVEL5'])
    df_cun = df.drop_duplicates(subset='cun')
    # print(df_cun)
    for index, row in df_cun.iterrows():
        try:
            level_collection = []
            for gridcode in range(1, 6):
                filtered_df = df[(df['cun'] == row['cun']) & (df['gridcode'] == gridcode)]
                level_collection.append(filtered_df['面积'].sum())
            area = round(sum(level_collection) / 666.67, 2)
            new_row: dict = {
                'sheng': row['sheng'],
                'sheng_code': row['sheng_code'],
                'shi': row['shi'],
                'shi_code': row['shi_code'],
                'xian': row['xian'],
                'xian_code': row['xian_code'],
                'zhen': row['zhen'],
                'zhen_code': row['zhen_code'],
                'cun': row['cun'],
                'cun_code': row['cun_code'],
                '面积（亩）': area,
                'LEVEL1': round(level_collection[0] * 100 / 666.67, 2),
                'LEVEL2': round(level_collection[1] * 100 / 666.67, 2),
                'LEVEL3': round(level_collection[2] * 100 / 666.67, 2),
                'LEVEL4': round(level_collection[3] * 100 / 666.67, 2),
                'LEVEL5': round(level_collection[4] * 100 / 666.67, 2)
            }
            new_df.loc[len(new_df)] = new_row
            level_collection.clear()
        except Exception as e:
            print(f"error:{e}")
    return new_df


def delshpfile(shp: str) -> None:
    try:
        os.remove(shp)
        os.remove(f"{shp.split('.')[0]}.cpg")
        os.remove(f"{shp.split('.')[0]}.dbf")
        os.remove(f"{shp.split('.')[0]}.prj")
        os.remove(f"{shp.split('.')[0]}.sbn")
        os.remove(f"{shp.split('.')[0]}.sbx")
        os.remove(f"{shp.split('.')[0]}.shx")
        os.remove(f"{shp}.xml")
    except Exception as e:
        print(f"error:{e}")


class ExportToExcel:
    def __init__(self, date, city, out_path):
        super().__init__()
        self.date = date
        self.city = city
        self.out_path = out_path
        self.cun_shp = CUN_SHP

    def Xlprocess(self) -> None:
        feature_shp_folder: str = fr"{self.out_path}/{self.city}/矢量"
        feature_name: str = fr"{feature_shp_folder}/{self.date}{self.city}.shp"
        out_feature: str = fr"{feature_shp_folder}/{self.date}{self.city}ZD.shp"
        print(out_feature)
        cun_shp: str = self.cun_shp
        if os.path.exists(out_feature):
            raise FileExistsError(f"{out_feature} has been created.")
        arcpy.analysis.SpatialJoin(feature_name, cun_shp,
                                   f"{out_feature}",
                                   "JOIN_ONE_TO_ONE", "KEEP_ALL",
                                   f'Id "Id" true true false 10 Long 0 10,First,'
                                   f'#,{feature_name},Id,-1,-1;gridcode "gridcode" true true false 10 Long 0 10,First,'
                                   f'#,{feature_name},gridcode,-1,-1;sheng "sheng" true true false 40 Text 0 0,First,'
                                   f'#,{cun_shp},sheng,0,40;shi "shi" true true false 40 Text 0 0,First,'
                                   f'#,{cun_shp},shi,0,40;xian "xian" true true false 40 Text 0 0,First,'
                                   f'#,{cun_shp},xian,0,40;zhen "zhen" true true false 40 Text 0 0,First,'
                                   f'#,{cun_shp},zhen,0,40;cun "cun" true true false 40 Text 0 0,First,'
                                   f'#,{cun_shp},cun,0,40;shi_code "shi_code" true true false 50 Text 0 0,First,'
                                   f'#,{cun_shp},shi_code,0,50;xian_code "xian_code" true true false 50 Text 0 0,First,'
                                   f'#,{cun_shp},xian_code,0,50;zhen_code "zhen_code" true true false 50 Text 0 0,First,'
                                   f'#,{cun_shp},zhen_code,0,50;cun_code "cun_code" true true false 50 Text 0 0,First,'
                                   f'#,{cun_shp},cun_code,0,50;sheng_code "sheng_code" true true false 50 Text 0 0,First,'
                                   f'#,{cun_shp},sheng_code,0,50',
                                   "LARGEST_OVERLAP", None, '')
        # 几何属性计算 这里输入要用绝对路径
        arcpy.management.CalculateGeometryAttributes(
            fr'{out_feature}',
            "面积 AREA", '', "SQUARE_METERS",
            'PROJCS["WGS_1984_UTM_Zone_50N",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Transverse_Mercator"],PARAMETER["False_Easting",500000.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",117.0],PARAMETER["Scale_Factor",0.9996],PARAMETER["Latitude_Of_Origin",0.0],UNIT["Meter",1.0]]',
            "SAME_AS_INPUT")

        excel_cun: pd.DataFrame = DataRead(out_feature)

        statisticians: pd.DataFrame = Read_table(excel_cun)
        statisticians_path: str = fr"{self.out_path}/{self.city}/统计表"
        os.makedirs(statisticians_path, exist_ok=True)
        print(fr"{statisticians_path}/{self.date}{self.city}早稻长势.xlsx")
        statisticians.to_excel(fr"{statisticians_path}/{self.date}{self.city}早稻长势.xlsx")
        delshpfile(feature_name)


def matched(match_cun: str, match_xian: str, mach_frame: pd.DataFrame) -> float:
    try:
        col_names = mach_frame.columns
        if 'cun' in col_names and 'xian' in col_names:
            filtered_df = mach_frame[(mach_frame['cun'] == match_cun) & (mach_frame['xian'] == match_xian)]
            return filtered_df['面积（亩）'].values[0]
        if '村' in col_names and '县' in col_names:
            filtered_df = mach_frame[(mach_frame['村'] == match_cun) & (mach_frame['县'] == match_xian)]
            return filtered_df['面积（亩）'].values[0]
        else:
            raise ValueError(fr"colums not in DataFrame")
    except Exception as e:
        print(e)


class TranslateExcel(ExportToExcel):
    def __init__(self, export_to_excel, area_exels_path):
        super().__init__(export_to_excel.date, export_to_excel.city, export_to_excel.out_path)
        self.to_trans_excel = fr"{self.out_path}/{self.city}/统计表/{self.date}{self.city}早稻长势.xlsx"
        self.after_trans_excel = fr"{self.out_path}/{self.city}/统计表/{self.date}{self.city}早稻长势2.xlsx"
        self.area_excel = pd.read_excel(fr"{area_exels_path}/江西省{self.city}.xlsx")


    def translate(self):
        new_df = pd.DataFrame(columns=['sheng', 'sheng_code',
                                       'shi', 'shi_code',
                                       'xian', 'xian_code',
                                       'zhen', 'zhen_code',
                                       'cun', 'cun_code',
                                       '面积（亩）',
                                    #    '面积（ndvi）',
                                       'LEVEL1', 'LEVEL2', 'LEVEL3', 'LEVEL4', 'LEVEL5'])
        # 读取每个县的每个村
        for index_excel, row_excel in pd.read_excel(self.to_trans_excel).iterrows():
            ndvi_arae_sum: float = sum(row_excel[['LEVEL1', 'LEVEL2', 'LEVEL3', 'LEVEL4', 'LEVEL5']].to_list())
            level_scale: list[float] = [i / ndvi_arae_sum
                                        for i in
                                        row_excel[['LEVEL1', 'LEVEL2', 'LEVEL3', 'LEVEL4', 'LEVEL5']].to_list()]
            # framland_area_sum: float = 0

            framland_area_sum: float = matched(match_cun=row_excel['cun'], match_xian=row_excel['xian'],
                                               mach_frame=self.area_excel)
            framland_area_sum = 0.0 if framland_area_sum is None else framland_area_sum

            if framland_area_sum == 0.0 or framland_area_sum is None:
                print(f"{row_excel['shi']}/{row_excel['xian']}/{row_excel['cun']}匹配失败")
                continue
            print(level_scale)
            level_area: list[float] = [
                area * framland_area_sum for area in level_scale
            ]
            new_row: dict = {
                'sheng': row_excel['sheng'],
                'sheng_code': row_excel['sheng_code'],
                'shi': row_excel['shi'],
                'shi_code': row_excel['shi_code'],
                'xian': row_excel['xian'],
                'xian_code': row_excel['xian_code'],
                'zhen': row_excel['zhen'],
                'zhen_code': row_excel['zhen_code'],
                'cun': row_excel['cun'],
                'cun_code': row_excel['cun_code'],
                '面积（亩）': framland_area_sum,
                # '面积（ndvi）': ndvi_arae_sum / 666.67,
                'LEVEL1': round(level_area[0], 2),
                'LEVEL2': round(level_area[1], 2),
                'LEVEL3': round(level_area[2], 2),
                'LEVEL4': round(level_area[3], 2),
                'LEVEL5': round(level_area[4], 2)
            }
            level_scale.clear()
            level_area.clear()
            new_df.loc[len(new_df)] = new_row
        return new_df

    def write(self):
        excel = self.translate()
        excel.to_excel(self.after_trans_excel, index=False)


if __name__ == "__main__":

    res = Crop_Growth(date="202405", city="九江市", frame_path="F:\企业实习\早稻地块数据", out_path="F:\企业实习\长势数据", tif_file=r"G:\jx_NDVI_05\JX_NDVI_05_reclass.tif")
    res.tif_to_shp()
    res2 = ExportToExcel(date="202405", city="九江市", out_path="F:\企业实习\长势数据")
    res3 = TranslateExcel(res2, area_exels_path=r"F:\企业实习\地块面积excel数据\水稻Excel")
    res3.Xlprocess()
    res3.write()
