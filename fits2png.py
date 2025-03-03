import os
from astropy.io import fits
from PIL import Image
import numpy as np
import cv2  # OpenCV用于Debayer处理

def debayer_fits(data, bayer_pattern='RGGB'):
    """
    对FITS文件中的Bayer模式数据进行去马赛克处理。
    
    :param data: FITS文件中的数据（2D数组）
    :param bayer_pattern: Bayer模式，默认为'RGGB'
    :return: 去马赛克后的彩色图像（3D数组，形状为[height, width, 3]）
    """
    # 将数据转换为8位（OpenCV要求输入为8位或16位）
    data_8bit = cv2.normalize(data, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    # 定义Bayer模式到OpenCV常量的映射
    bayer_patterns = {
        'RGGB': cv2.COLOR_BayerRG2RGB,
        'BGGR': cv2.COLOR_BayerBG2RGB,
        'GRBG': cv2.COLOR_BayerGR2RGB,
        'GBRG': cv2.COLOR_BayerGB2RGB,
    }

    # 检查Bayer模式是否有效
    if bayer_pattern not in bayer_patterns:
        raise ValueError(f"Unsupported Bayer pattern: {bayer_pattern}. Supported patterns are: {list(bayer_patterns.keys())}")

    # 去马赛克处理
    color_image = cv2.cvtColor(data_8bit, bayer_patterns[bayer_pattern])
    return color_image

def fits_to_png(fits_path, png_path, bayer_pattern='RGGB', brightness_gain=1.5, rotate_180=False):
    """
    将FITS文件转换为PNG格式，支持Debayer处理、亮度调整和旋转。
    
    :param fits_path: FITS文件路径
    :param png_path: 输出的PNG文件路径
    :param bayer_pattern: Bayer模式，默认为'RGGB'
    :param brightness_gain: 亮度增益，默认为1.5
    :param rotate_180: 是否将图像向右旋转180度，默认为False
    """
    # 读取FITS文件
    with fits.open(fits_path) as hdul:
        data = hdul[0].data

    # 去马赛克处理
    color_image = debayer_fits(data, bayer_pattern=bayer_pattern)

    # 调整亮度
    color_image = np.clip(color_image * brightness_gain, 0, 255).astype(np.uint8)

    # 创建PIL图像
    image = Image.fromarray(color_image)

    # 如果需要旋转180度
    if rotate_180:
        image = image.rotate(180, expand=True)  # 旋转180度

    # 保存为PNG
    image.save(png_path)

def batch_convert_fits_to_png(input_folder, output_folder, bayer_pattern='RGGB', brightness_gain=1.5, rotate_180=False):
    """
    批量将FITS文件转换为PNG格式，支持Debayer处理、亮度调整和旋转。
    
    :param input_folder: 输入文件夹路径（包含FITS文件）
    :param output_folder: 输出文件夹路径（保存PNG文件）
    :param bayer_pattern: Bayer模式，默认为'RGGB'
    :param brightness_gain: 亮度增益，默认为1.5
    :param rotate_180: 是否将图像向右旋转180度，默认为False
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有FITS文件
    for filename in os.listdir(input_folder):
        if filename.endswith('.fits') or filename.endswith('.fit'):
            fits_path = os.path.join(input_folder, filename)
            png_path = os.path.join(output_folder, filename.replace('.fits', '.png').replace('.fit', '.png'))
            fits_to_png(fits_path, png_path, bayer_pattern=bayer_pattern, brightness_gain=brightness_gain, rotate_180=rotate_180)
            print(f'Converted {fits_path} to {png_path} with Bayer pattern {bayer_pattern}, brightness gain {brightness_gain}, and rotate_180={rotate_180}')

# 使用示例
input_folder = 'D:/天宫/lights'
output_folder = 'D:/天宫/pngs'
bayer_pattern = 'RGGB'  # 根据相机设置调整Bayer模式
brightness_gain =5.0  # 调整亮度增益
rotate_180 = True  # 是否旋转180度
batch_convert_fits_to_png(input_folder, output_folder, bayer_pattern=bayer_pattern, brightness_gain=brightness_gain, rotate_180=rotate_180)