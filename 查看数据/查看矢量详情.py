import geopandas as gpd
import matplotlib.pyplot as plt
from asset.Global import DataRead
import contextily as ctx


class ShowShapefile:
    def __init__(self, path):
        self.path = path
        self.gdf = gpd.read_file(self.path).to_crs(epsg=3857)

    def get_shp_info(self):
        return DataRead(self.path)

    def show(self):
        fig, ax = plt.subplots(figsize=(15, 15))  # 调整图的大小
        self.gdf.boundary.plot(ax=ax, alpha=0.5, edgecolor='k')
        ctx.add_basemap(ax, source='http://t0.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=64b19b3a8cb3b3e905831203b1306beb')
        ax.axis('off')  # 去掉坐标轴
        plt.show()


