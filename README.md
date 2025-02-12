# 江西农业监测系统开发

在**江西农业监测系统开发**项目进行的过程中，团队需要对大量矢量数据进行筛选、确认、处理以及外派确认数据存疑区域。特此作一个简易的程序提高团队效率。

## 1.数据处理部分

### 主要使用tkinter+arcpy

#### 使用前提：

###### 1）更改asset\Global.py中两处地方。

```
CUN_SHP = r"F:\企业实习\早稻\长势数据提交\江西村边界.shp"
jiangxi_cities: list[str] = ["南昌市", "九江市", "上饶市", "抚州市", "宜春市", "吉安市", "赣州市", "景德镇市", "萍乡市", "新余市", "鹰潭市"]
```

###### 2）若是在arcgis pro的环境下，需要下载geopandas，否则将”查看数据\查看矢量详情.py“内的geopandas相关给注释掉且不能使用查看矢量的功能。

###### 在main.py中引入了sv_ttk，如果不想引用可以注释掉 import以及  sv_ttk.set_theme("light")

###### 3）引入的包：

```
\ArcGIS\Pro\Resources\ArcPy
```

<img src="image/image.png" alt="image" style="zoom:50%;" />

## 2.外出作业检查数据部分

### 主要使用flask框架进行后端搭建

###### 1）使用PostgreSQL数据库对江西省田块数据进行分片储存, geojson、shapely、pyproj、math等在数据输出时对地理数据进行投影转换。

<img src="image\image2.png" alt="image-20250212193110124" style="zoom: 25%;" />

<video src="image\draft.mp4" style="zoom: 70%;"></video>
