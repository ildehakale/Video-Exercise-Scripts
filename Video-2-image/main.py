
import argparse
from Video2image import Video2Image
import logging
# STEP BY STEP GUIDE:
# =========================
# ARCHITECTURE:
"""
video2image.py -> calls Video2image  ->  input video file -> extract frames with cv2 
-> save frames as images in output file by specified fps

"""
# ========================
# video to image with mp4 format videos
# select the video path and output image path
# select the number of frame per second by parse argument
# import logger to log the process


def parse_args():
    parser = argparse.ArgumentParser(description='Video to Image by specified fps')

    parser.add_argument('--video-path', 
                        type=str, 
                        required=True,
                        help='Path to the input video file')
    parser.add_argument('--output-path',
                        type=str,
                        required=True,
                        help='Path to the output image directory')
    parser.add_argument('--fps',
                        type=int,
                        default=1,
                        help=' Number of frames to extract per second')
    
    return parser.parse_args()



def main():
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='./video2image.log', # 
                    filemode='w')
    
    args= parse_args()

    video2Image = Video2Image(args.video_path, args.output_path, args.fps)

    video2Image.extract_frames()


    
if __name__ == '__main__':
    main()