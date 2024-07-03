import geopandas as gpd
import matplotlib.pyplot as plt
from asset.Global import DataRead


class ShowShapefile:
    def __init__(self, path):
        self.path = path
        self.gdf = gpd.read_file(self.path)

    def get_shp_info(self):
        return DataRead(self.path)

    def show(self):
        self.gdf.plot()
        plt.show()



