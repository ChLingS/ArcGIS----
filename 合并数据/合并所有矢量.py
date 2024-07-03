import multiprocessing
import arcpy
import os


def merge_shp_files(city: str) -> None:
    print(f"{city}start")
    folder_path: str = fr"5Data-base/{city}/矢量"
    # 获取文件夹中所有的shp文件
    shp_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.shp')]

    # 合并所有的shp文件
    outfolder: str = f"5月/{city}/矢量"
    os.makedirs(outfolder, exist_ok=True)

    arcpy.Merge_management(inputs=shp_files, output=f"{outfolder}/{city}.shp")


def merge_all_shp_files(folder_path, out_path):
    # 获取文件夹及其子文件夹中所有的shp文件
    shp_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.shp'):
                shp_files.append(os.path.join(root, file))
    # 合并所有的shp文件
    arcpy.Merge_management(inputs=shp_files, output=f"{out_path}")


def merge_all_tif(folder_path, out_path, out_tif):
    tif_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.tif'):
                tif_files.append(os.path.join(root, file))

    arcpy.MosaicToNewRaster_management(input_rasters=tif_files, output_location=out_path, raster_dataset_name_with_extension=out_tif, number_of_bands=1)


if __name__ == "__main__":
    # jiangxi_cities: list[str] = ["南昌市", "九江市", "上饶市", "抚州市", "宜春市", "吉安市", "赣州市", "景德镇市", "萍乡市",
    #                   "新余市", "鹰潭市"]
    # with multiprocessing.Pool(11) as pool:
    #     pool.map(
    #         merge_shp_files, jiangxi_cities
    #     )
    # merge_all_shp_files('5月')
    # merge_shp_files('九江市')
    # merge_all_shp_files(r'F:\企业实习\原始地块（全省）\江西省耕地地块数据\赣州市')
    merge_all_tif(r"/5Data-base/抚州市/栅格")