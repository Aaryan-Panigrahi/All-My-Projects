import cv2 as cv
import numpy as np
import os
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from collections import deque


# Clustering contours based on closeness (Aglomerative CLustering)

def agglomerative_cluster(contours, threshold_d = 40.0):
    current_contours = contours

    while len(current_contours) > 1:
        min_distance = None
        min_coordinate = None

        for x in range(len(current_contours)-1):
            for y in range(x+1, len(current_contours)):
                distance = calculate_contour_distance(current_contours[x], current_contours[y])
                if min_distance is None:
                    min_distance = distance
                    min_coordinate = (x, y)
                elif distance < min_distance:
                    min_distance = distance
                    min_coordinate = (x, y)

        if min_distance < threshold_d : 
            index1, index2 = min_coordinate
            current_contours[index1] = merge_contours(current_contours[index1], current_contours[index2])
            del current_contours[index2]
        else: 
            break

    return current_contours

def calculate_contour_distance(c1, c2): 
    x1, y1, w1, h1 = cv.boundingRect(c1)
    c_x1 = x1 + w1/2
    c_y1 = y1 + h1/2

    x2, y2, w2, h2 = cv.boundingRect(c2)
    c_x2 = x2 + w2/2
    c_y2 = y2 + h2/2

    return max(abs(c_x1 - c_x2) - (w1 + w2)/2, abs(c_y1 - c_y2) - (h1 + h2)/2)

def merge_contours(c1, c2):
    return np.concatenate((c1, c2), axis=0)

#Video Capture
cap = cv.VideoCapture('tennisVid.mp4')
out = cv.VideoWriter('output_v3-1.mp4', cv.VideoWriter_fourcc(*'mp4v'), 30, (1920, 1080))

#Region of intrest
def roi(frame, vertices):
    mask = np.zeros_like(frame)
    channel_count = frame.shape[2]
    match_mask_color = (255,) * channel_count
    cv.fillPoly(mask, vertices, match_mask_color)
    masked = cv.bitwise_and(frame, mask)
    return masked

roi_vertices = [
    (110, 860),
    (1760, 860),
    (1310, 165),
    (555, 165)
]

#HSV range of the the ball
lower_color = np.array([40, 0, 121])
upper_color = np.array([104, 177, 255])

ret, f1 = cap.read()
ret, f2 = cap.read()

#A deque will store the trail of coordinates of our ball
deq = deque(maxlen=100)

while cap.isOpened():
    
    #HSV Filters
    hsv1 = cv.cvtColor(f1, cv.COLOR_BGR2HSV)
    mask1 = cv.inRange(hsv1, lower_color, upper_color)
    res1 = cv.bitwise_and(f1, f1, mask=mask1)

    hsv2 = cv.cvtColor(f2, cv.COLOR_BGR2HSV)
    mask2 = cv.inRange(hsv2, lower_color, upper_color)
    res2 = cv.bitwise_and(f2, f2, mask=mask2)

    # I found the results to be better without the hsv filters, so I commented them out
    #diff = cv.absdiff(res1, res2)

    #Finding the difference to detect motion beween frames
    diff = cv.absdiff(f1, f2)

    roi_frame = roi(diff, np.array([roi_vertices], np.int32))

    #Preprocessing the frame
    gray = cv.cvtColor(roi_frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv.threshold(blur, 20, 255, cv.THRESH_BINARY)
    dialated = cv.dilate(thresh, None, iterations=3)

    #Finding contours
    contours, _ = cv.findContours(dialated, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    contours = list(contours)
    contours = agglomerative_cluster(contours, threshold_d =20.0)
    
    

    for contour in contours:

        (x,y,w,h) = cv.boundingRect(contour)

        cv.rectangle(f1, (x,y), (x+w, y+h), (255,0,0), 2)        

        #The bigger objects have been clustered together and can be filtered out by size
        if cv.contourArea(contour) < 850:
            cv.rectangle(f1, (x,y), (x+w, y+h), (0,255,0), 2)
            c_x = int(x+w/2)
            c_y = int(y+h/2)
            cv.circle(f1, (c_x, c_y), 6, (0,0,255), -1)
        
            deq.appendleft((c_x, c_y))
            prev_pt = (c_x, c_y)
            for pt in deq:
                #cv.line(f1, prev_pt, pt, (0,0,255), 2)
                cv.circle(f1, pt, 6, (0,0,255), -1)
    

    #cv.drawContours(f1, contours, -1, (0,255,0), 2)

    #cv.imshow('dialated', dialated)
    #cv.imshow('diff', diff)
    cv.imshow('f1', f1)
    out.write(f1)
    
    #Going to the next two frames
    f1 = f2
    ret, f2 = cap.read()

    if cv.waitKey(60) & 0xFF == 27:
        break

cv.destroyAllWindows()
out.release()
cap.release()