import os
import rasterio
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import mapping


# 读取 Shapefile 文件
def read_shapefile(shapefile_path):
    shapefile = gpd.read_file(shapefile_path)
    return shapefile


# 根据 Shapefile 裁剪 TIFF 文件
def clip_tiff(tiff_file, shapefile, output_file):
    with rasterio.open(tiff_file) as src:
        # 获取 Shapefile 的几何信息
        geometries = [mapping(geom) for geom in shapefile.geometry]
        # 裁剪 TIFF 文件
        out_image, out_transform = mask(src, geometries, crop=True)
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform
        })

        with rasterio.open(output_file, "w", **out_meta) as dest:
            dest.write(out_image)


# 遍历目录并裁剪所有 TIFF 文件
def process_tiff_files(tiff_dir, output_dir, shapefile):
    for root, _, files in os.walk(tiff_dir):
        for filename in files:
            if filename.lower().endswith((".tif", ".tiff")):
                tiff_file = os.path.join(root, filename)
                relative_path = os.path.relpath(tiff_file, tiff_dir)
                output_file = os.path.join(output_dir, relative_path)
                output_folder = os.path.dirname(output_file)

                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                clip_tiff(tiff_file, shapefile, output_file)
                print(f"Clipped {tiff_file} to {output_file}")


# 示例用法
tiff_dir = r'C:\Users\cumin\Desktop\2.数据处理\To_TIFF'
shapefile_path = r'C:\Users\cumin\Desktop\1.下载数据\内蒙古矢量边界_草地类型\Export_Output.shp'
output_dir = r'C:\Users\cumin\Desktop\2.数据处理\Clip_TIFF'

# 读取 Shapefile
shapefile = read_shapefile(shapefile_path)

# 处理所有 TIFF 文件
process_tiff_files(tiff_dir, output_dir, shapefile)
