import cv2
import os
import argparse
from PIL import Image

def extract_first_frame(video_path, output_path):
    # 打开视频文件
    video = cv2.VideoCapture(video_path)
    
    # 检查视频是否成功打开
    if not video.isOpened():
        print(f"Error opening video file {video_path}")
        return
    
    # 读取第一帧
    ret, frame = video.read()
    
    if ret:
        # 如果成功读取帧
        # 将OpenCV的BGR格式转换为RGB格式
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 创建PIL Image对象
        pil_image = Image.fromarray(frame_rgb)
        
        # 保存帧为PNG
        pil_image.save(output_path, 'PNG')
        print(f"First frame saved to {output_path}")
    else:
        print(f"Failed to extract frame from {video_path}")
    
    # 释放视频对象
    video.release()

def main():
    parser = argparse.ArgumentParser(description="Extract the first frame from an AVI video as PNG.")
    parser.add_argument("--input", default='data/0X1A0A263B22CCD966.avi', help="Path to the input AVI video file")
    parser.add_argument("-o", "--output", default='data/cond_frame0.jpg', help="Path to save the output PNG file (default: same as input with .png extension)")
    
    args = parser.parse_args()
    
    input_path = args.input
    
    if args.output:
        output_path = args.output
    else:
        # 如果没有指定输出路径，使用输入文件名但更改扩展名为.png
        output_path = os.path.splitext(input_path)[0] + ".png"
    
    extract_first_frame(input_path, output_path)

if __name__ == "__main__":
    main()