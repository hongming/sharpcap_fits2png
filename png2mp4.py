import os
import subprocess

# 设置图片目录和输出视频文件路径
image_dir = r"D:\tiangong\pngs"
output_video = r"D:\tiangong\output.mp4"

# 设置帧率 (假设15秒内播放完所有图片)
image_count = len([f for f in os.listdir(image_dir) if f.endswith('.png')])
frame_rate = image_count / 15  # 计算合适的帧率

# 生成 ffmpeg 命令
ffmpeg_cmd = [
    "ffmpeg",
    "-framerate", str(frame_rate),  # 设置帧率
    "-i", os.path.join(image_dir, "%03d.png"),  # 需要确保文件命名是 00001.png, 00002.png ... 这样有序
    "-c:v", "libx264",  # 使用 H.264 编码
    "-pix_fmt", "yuv420p",  # 兼容性更好的像素格式
    "-y", output_video  # 输出文件
]

# 执行 ffmpeg 命令
subprocess.run(ffmpeg_cmd, shell=True)
print(f"视频已生成：{output_video}")
