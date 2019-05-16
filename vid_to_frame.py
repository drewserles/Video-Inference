import os
import cv2
import matplotlib.pyplot as plt
import time
import math

def extractImages(src_dir, vid_name, fps, write_dir):
    '''
    src_dir: Video source path
    vid_name: Video filename
    fps: Number of frames to make from each second of video (frequency)
    write_dir: Path to write frames to
    '''
    s1 = time.time()
    # Create the write directory if necessary
    if not os.path.exists(write_dir):
        os.makedirs(write_dir)
    
    img_prefix = vid_name[:vid_name.index('.')]

    cap = cv2.VideoCapture(src_dir+ '/' + vid_name)
    frameRate = cap.get(cv2.CAP_PROP_FPS) # Frame rate of this video
    frameFreq = int(frameRate / fps)      # Write a frame every frameFreq'th frame in video
    
    count = 0
    while(cap.isOpened()):
        frameId = cap.get(cv2.CAP_PROP_POS_FRAMES) #current frame number
        ret, frame = cap.read()
        if (ret != True):
            break
        # Save a frame once every "frame frequency"
        if (frameId % frameFreq == 0):
            count += 1
            filename = f'{write_dir}/{img_prefix}_{count}.jpg'
            grey_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(filename, grey_frame)
    cap.release()

    print(f'Done! Wrote {count} images from {src_dir}{vid_name} to {write_dir} in {time.time() - s1:.2f} sec.')


def writeFunc(path_list, fps_to_save):
    '''
    Take in a list of lists and a fps save rate. Each list items is a pair of directories. The first is the source
    directory of videos to be converted to frames. The second is the write directory that frames will go to.

    path_list: [[src_path, write_path], ...]
    fps_to_save: Number of frames to make from each second of video (frequency)
    '''
    for path_pair in path_list:
        src_path, write_path = path_pair[0], path_pair[1]
        vids = os.listdir(src_path)
        for v in vids:
            extractImages(src_path, v, fps_to_save, write_path)  
        print("- - - - - - -")