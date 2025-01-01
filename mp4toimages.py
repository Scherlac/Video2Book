
# we load the 2023-11-21_14h18_21.mp4 file and process each frame one by one to see there is a change on the video
#%pip install opencv-python
#%pip install numpy

import cv2
import numpy as np
import os
import sys
import time
import datetime


def detect_content(ver_std):
    # threshold for the std deviation
    mean_ver_str = np.mean(ver_std)
    std_ver_str = np.std(ver_std)

    hi = np.array(ver_std > mean_ver_str)
    ver = np.array(ver_std)
    hi_mean = np.mean(ver[hi])
    hi_std = np.std(ver[hi])
    low_mean = np.mean(ver[~hi])
    low_std = np.std(ver[~hi])

    hi = np.array(ver_std > (low_mean + 3*low_std))

    # we detect the range of the strip with high std deviation
    with open('content.dat', 'w') as f:
        print(ver_std, file=f)

    # the range of the strip with high std deviation
    min_x = np.min(np.where(hi))
    max_x = np.max(np.where(hi))

    return min_x, max_x


def collect_content(gray, width):
    """
    Detects the content of the image by calculating the standard deviation of the vertical strips of the image.
    """
    ver_std = []
    ver_mean = []
    # check 10px width vertical strips on the image and calculate the std deviation
    for x in range(0, width, 10):
        strip = gray[:, x:x+10]
        std = 255 - np.mean(strip)
        ver_std.append(std)

    return np.array(ver_std)

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

    first_frame = True

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
        # log_file.write(msg + '\n')
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

            ver_std = collect_content(gray, width)

            if first_frame:
                average_ver = ver_std
                first_frame = False
            else:
                average_ver = (average_ver * 0.99 + ver_std * 0.01)


    average_min_x, average_max_x = detect_content(average_ver)

    print(f"min_x: {average_min_x}, max_x: {average_max_x}")


