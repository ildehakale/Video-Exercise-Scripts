import os
import cv2
import logging
import sys
from concurrent.futures import ThreadPoolExecutor

class Video2Image:

    def __init__(self, video_path, output_path, fps,type):
        self.video_path = video_path
        self.output_path = output_path
        self.fps=fps
        self.type=type
        self.logger = logging.getLogger('Video2Image')

            
    def input_video(self):
        cap= cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            self.logger.error(f"Error opening video file : {self.video_path}")
            sys.exit(1)

        return cap
    
    def input_fps(self):

        if self.fps <=0:
            self.logger.warning(f"Invalid fps value: {self.fps}. Setting to default fps=1")
            video_fps=1
        else:
            video_fps= self.fps
        
        return video_fps
    
    def output_image_path(self):
        
        # if no outputh path exist, create a new folder
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)
            self.logger.info(f"Created output directory: {self.output_path}")

        image_path = os.path.join(self.output_path)

        return image_path
    
    def get_type(self):
        file_format = self.type
        self.logger.info(f"Image type format: {file_format}")
        return file_format
    
    """
    The maths behind extract_frames:

    Lets say total_frames is 750 frames, original_video_fps is 25.
    if we  say --fps 1 ,  we will save every 25th frame (25/1=25).
    750/25=30 png files will be saved. 
    """
    def extract_frames(self):

        cap = self.input_video()
        video_fps = self.input_fps()
        image_format =self.get_type()

        output_path = self.output_image_path()

        # count frames to be saved
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.logger.info(f"Total frames in video: {total_frames}")
        saved_frame_count = 0
        # get original video fps
        video_original_fps = cap.get(cv2.CAP_PROP_FPS)
        self.logger.info(f"Original video FPS: {video_original_fps}")
        # calculate frame interval
        frame_interval = video_original_fps / video_fps
        self.logger.info(f"Frame interval for extraction: {frame_interval}")
        # initialize the next frame to save
        next_frame_to_save = 0
        # use thread pool executor for saving frames and improve performance
        with ThreadPoolExecutor(max_workers=4) as executor:
            while True:

                ret , frame = cap.read()
                
                if not ret: 
                    self.logger.info("End of video file reached or cannot read the video file.")
                    break

                current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                current_frame_zero = current_frame - 1

                # print(current_frame)
                if current_frame > total_frames and total_frames > 0:
                    self.logger.info("Reached the desired number of frames to save.")
                    break

                image_path = self.output_path
                # why 0.01? to avoid floating point precision issues
                if current_frame_zero >= next_frame_to_save- 0.01:
                    try:
                        cv2.imwrite(os.path.join(image_path, f"frame_{saved_frame_count:05d}.{image_format}"), frame)
                    except cv2.error as e:
                        self.logger.error(f"Error saving frame {saved_frame_count} at {image_path}: {e}")
                        continue
                    except IOError as e:
                        self.logger.error(f"I/O error saving frame {saved_frame_count} at {image_path}: {e}")
                        break
                    # Use executor to save frame asynchronously
                    executor.submit(cv2.imwrite, os.path.join(image_path, f"{saved_frame_count:05d}.{image_format}"), frame)
                    self.logger.debug(f"Submitted frame {saved_frame_count} for saving.")

                    # update saved frame count
                    saved_frame_count += 1
                    self.logger.info(f"Saved frame {saved_frame_count} at {image_path}")
                    # update the next frame to save
                    next_frame_to_save += frame_interval
                if total_frames > 0 and current_frame >= total_frames:
                    self.logger.info("Reached the end of the last frame.")
                    break

        cap.release()
        self.logger.info("Released video capture object.")

        total_frames = saved_frame_count
        self.logger.info(f"Total frames saved: {total_frames}")