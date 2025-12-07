import os 
import cv2
import logging 
import sys
from concurrent.futures import ThreadPoolExecutor


class Image2video:

    def __init__(self,image_path, output_path):

        self.image_path = image_path
        self.output_path = output_path
        self.logger = logging.getLogger('Video2Image')

    def input_image_file(self):

        image_file_path = self.image_path
        if not image_file_path:
            self.logger.error(f"Error opening image file: {image_file_path}")
        else:
            image_file = os.path.join(image_file_path)
            self.logger.info(f"Image file located at : {image_file}")

        return image_file
    

    def output_video_file(self):
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
            self.logger.info(f"Created output directory.")

        video_path = os.path.join(self.output_path)
        self.logger.info(f"Output video file located at : {video_path}")
        return video_path
    
    def image_to_video(self):

        """
        read image file 
        convert it to mp4v with cv2
        read them with threadpool with 4 threads at the same time
        write them on for loop 

        """
        # get input and output files
        image_file = self.input_image_file()
        output_file = self.output_video_file()
        # read image file 
        read_image_file = [f for f in os.listdir(image_file) 
                           if f.endswith((".png",".jpg", ".jpeg"))]
        self.logger.info(f"Image file succesffully read.")

        # frame per second for video
        fps= 25
        # size of video
        size = (1920,1080)
        # video name and join the video into the output folder 
        video_name = os.path.join(output_file,"video.mp4")
        # write the video with cv2
        output_video = cv2.VideoWriter(video_name, 
                                       cv2.VideoWriter_fourcc(*"mp4v"),
                                       fps, size, True)
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            # execute the list with 4 thread so now 4 images works at the same time 
            images = list(executor.map(lambda i: cv2.imread(os.path.join(image_file,i)), 
                                       read_image_file))
            self.logger.info(f"Total images loaded: {len([i for i in images])}")
                
        for img in images:
            if img is not None:
                output_video.write(img)
            else:
                self.logger.error(f"Cannot read the img to make the video.")

        output_video.release()
        self.logger.info(f"Video succesffully created.")


        




