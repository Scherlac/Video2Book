
# we load the 2023-11-21_14h18_21.mp4 file and process each frame one by one to see there is a change on the video
#%pip install opencv-python
#%pip install numpy

import cv2
import numpy as np
import os
import sys
import time
import datetime

def mp4toimages(path, out_folder):
    """Converts the mp4 file to jpg images and saves them to the out folder."""

    # we load the video file
    cap = cv2.VideoCapture(path)

    # we get the number of frames
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # we get the frame rate
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # we get the duration of the video
    duration = frame_count/fps

    # we get the width and height of the video

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # we get the codec of the video
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))

    # initialize the variables for the rapid calculation of standard deviation
    A = 0
    Q = 0.2
    k = 0
    S = 0

    frame_mean_change = 0

    M = 1
    MM = 0
    prev_gray = None


    # for each frame we process it
    for i in range(frame_count):
        # we get the frame
        ret, frame = cap.read()
        # we convert the frame to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_gray is None:
            prev_gray = gray
            continue

        # we get the difference between the current frame and the previous one
        diff = cv2.absdiff(gray, prev_gray)
        # we get the mean of the difference
        frame_mean_change = np.mean(diff)

        # we save the current frame as the previous one
        prev_gray = gray

        # we write the mean of the difference between the frames to log file
        msg = f'\rframe: {i}, change: {frame_mean_change}, std dev: {S}'
        log_file.write(msg + '\n')
        print(msg)


        # update the calculation for the rapid calculation of standard deviation
        k = k + 1
        A1 = A + ( frame_mean_change - A ) / k
        Q = Q + ( frame_mean_change - A ) * ( frame_mean_change - A1 ) 
        A = A1
        S = np.sqrt(Q / k)

        # if the mean is greater than a threshold, we trigger the saving of the frame
        if frame_mean_change > 1.5*S:
            M = M + 1

        # we save the frame to file if M is larger than MM and the mean is small so we have a stable video    
        if M > MM and frame_mean_change < 0.4 * S:
            cv2.imwrite(f'{out_folder}/img_{M:05d}.jpg', frame)
            MM = M




# we open the log file
log_file = open('log.txt', 'w')


mp4toimages('WP_20231226_12_03_50_Pro.mp4', 'out')

# we close the log file
log_file.close()

