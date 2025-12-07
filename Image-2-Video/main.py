# main.py

"""
Image2Video script

Take all images from images file and convert it to a mp4 video format

Take the parameters :  --image-path, --output-path , 


"""
"""
Terminal command:
python3 main.py --image-path ./images --output-path ./videos

"""
import argparse
import logging
from Image2Video import Image2video

def parse_args():
    parser = argparse.ArgumentParser(description=' Image to Video ')

    parser.add_argument('--image-path',
                        type=str,
                        required=True,
                        help= 'Path to input image file')
    parser.add_argument('--output-path',
                        type=str,
                        required=True,
                        help='Path to output of video ')
    
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO,
                        format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s', # log file format
                        filename ='./image2video.log', # log file path                        
                        filemode = 'w') # write mode
    
    args = parse_args()

    image2Video = Image2video(args.image_path, args.output_path)

    image2Video.image_to_video()


if __name__ == '__main__':
    main()




