import os
import numpy as np
from PIL import Image


# 读取 ASCII 文件并跳过头信息
def read_ascii_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith(
                    ('ncols', 'nrows', 'xllcorner', 'yllcorner', 'cellsize', 'NODATA_value', 'xllcenter', 'yllcenter')):
                continue
            try:
                row = list(map(float, line.split()))
                data.append(row)
            except ValueError as e:
                print("Error converting line to float: {line}")
                raise e
    return np.array(data)


# 将 ASCII 数据转换为图像并保存为 TIFF
def ascii_to_tiff(ascii_file, tiff_file):
    data = read_ascii_file(ascii_file)
    image = Image.fromarray(data.astype(np.float32))  # 假设数据是浮点数
    image.save(tiff_file, format='TIFF')


# 遍历目录并转换所有文件
def convert_all_files(ascii_dir, tiff_dir):
    if not os.path.exists(tiff_dir):
        os.makedirs(tiff_dir)

    for filename in os.listdir(ascii_dir):
        if filename.endswith(".txt"):
            ascii_file = os.path.join(ascii_dir, filename)
            tiff_file = os.path.join(tiff_dir, filename.replace(".txt", ".tiff"))
            ascii_to_tiff(ascii_file, tiff_file)
            print("Converted {ascii_file} to {tiff_file}")


ascii_dir = r'C:\Users\cumin\Desktop\1.download_data\中国雪深长时间序列数据集（1979-2023）\snow depth\snowdepth-1979'
tiff_dir = r'C:\Users\cumin\Desktop\2.processing_data\ASCII_to_TIFF\1979'

convert_all_files(ascii_dir, tiff_dir)