import cv2
import os
import argparse

def get_video_info(video_path):
    # 打开视频文件
    video = cv2.VideoCapture(video_path)
    
    # 检查视频是否成功打开
    if not video.isOpened():
        print(f"Error opening video file {video_path}")
        return None
    
    # 获取视频的宽度和高度
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    # 获取视频的总帧数
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # 获取视频的帧率
    fps = video.get(cv2.CAP_PROP_FPS)
    
    # 计算视频时长（秒）
    duration = frame_count / fps
    
    # 获取文件大小（字节）
    file_size = os.path.getsize(video_path)
    
    # 释放视频对象
    video.release()
    
    return {
        "width": width,
        "height": height,
        "frame_count": frame_count,
        "fps": fps,
        "duration": duration,
        "file_size": file_size
    }

def main():
    parser = argparse.ArgumentParser(description="Get information about an MP4 video file.")
    parser.add_argument("--input", default="/mnt/zhen_chen/cxli/dataset/EchoNet-Dynamic/Videos/0X1A0A263B22CCD966.avi",help="Path to the input MP4 video file")
    
    args = parser.parse_args()
    
    video_info = get_video_info(args.input)
    
    if video_info:
        print(f"Video resolution: {video_info['width']}x{video_info['height']}")
        print(f"Frame count: {video_info['frame_count']}")
        print(f"FPS: {video_info['fps']:.2f}")
        print(f"Duration: {video_info['duration']:.2f} seconds")
        print(f"File size: {video_info['file_size'] / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    main()