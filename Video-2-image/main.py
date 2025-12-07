
import argparse
import logging
from Video2image import Video2Image
# =========================

# ARCHITECTURE:
"""
video2image.py -> calls Video2image  ->  input video file -> extract frames with cv2 
-> save frames as images in output file by specified fps

"""
# ========================

# STEP BY STEP GUIDE:
# video to image with mp4 format videos
# import Video2image class to handle video to image conversion
# import logger to log the process

# select video-path , output-path and the number of frame per second(fps) by parse argument
# find all images in your images file
"""
Terminal Command:

python3 main.py --video-path ./sample_videos/sample1.mp4 --output-path ./images --fps 1 --type png


Expected Output:
Extracted frames will be saved as images in the specified output directory at the rate of 1 frame per second.


"""

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
    parser.add_argument('--type',
                        type=str,
                        default='png',
                        help= 'Format of the image files (e.g. png,jpg,jpeg)')
    
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # log file format 
                    filename='./video2image.log', # log file path
                    filemode='w' ) # write mode 
    
    args= parse_args()

    video2Image = Video2Image(args.video_path, args.output_path, args.fps,args.type)

    video2Image.extract_frames()


if __name__ == '__main__':
    main()