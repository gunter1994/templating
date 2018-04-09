import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt
import os
from skimage.transform import pyramid_gaussian
from skimage.io import imread
from skimage.feature import hog
from sklearn.externals import joblib

def intersect(rect1, rect2):
    # Calculate the total area both rectangles intersect
    x_inter = max(0, min(rect1[2], rect2[2]) - max(rect1[0], rect2[0]))
    y_inter = max(0, min(rect1[3], rect2[3]) - max(rect1[1], rect2[1]))
    intersectA = x_inter * y_inter
    rect1A = (rect1[2] - rect1[0]) * (rect1[3] - rect1[1])
    rect2A = (rect2[2] - rect2[0]) * (rect2[3] - rect2[1])
    nonIntersect = rect1A + rect2A - intersectA
    return max(intersectA / float(nonIntersect),intersectA/rect1A,intersectA/rect2A) #encase an entire rect is engulfed by another

def nms(class1,class2, threshold):
	c1 = class1[:]
	c2 = class2[:]
    #first check for inter class overlap
	for i in class1:
		for j in class2:
			if i in c1 and j in c2:
				if intersect(i,j) > threshold:
					if i[5][0][1] < j[5][0][2]:
						c1.remove(i)
					else:
						c2.remove(j)
	#check for own class collisions
	for i in class1:
		for j in class1[class1.index(i)+1:]:
			if i in c1 and j in c1:
				if intersect(i,j) > threshold:
					if i[5][0][1] < j[5][0][1]:
						c1.remove(i)
					else:
						c1.remove(j)
	#check for own class collisions
	for i in class2:
		for j in class2[class2.index(i)+1:]:
			if i in c2 and j in c2:
				if intersect(i,j) > threshold:
					if i[5][0][2] < j[5][0][2]:
						c2.remove(i)
					else:
						c2.remove(j)
	return (c1,c2)

def check_phone(img):
	window_size = (80, 160)
	step = (10, 10)

	clf = joblib.load('model.pkl')

	apple = []
	samsung = []
	pyr = 0
	ds = 1.25

	imgP = pyramid_gaussian(img, downscale=ds)
	for im in imgP:
		if im.shape[0] < window_size[1] or im.shape[1] < window_size[0]:
			break
		for x in range(0,im.shape[0],step[0]):
			for y in range(0,im.shape[0],step[1]):
				window = im[y:y+window_size[1],x:x+window_size[0]]
				if window.shape[0] != window_size[1] or window.shape[1] != window_size[0]:
					continue
				X_ = hog(window, 9, [8,8], [3,3])
				X_ = X_.reshape(1,-1)
				Y_ = clf.predict(X_)
				if Y_ == 1:
					apple.append((x, y, x+int(window_size[0]), y+int(window_size[1]),(ds**pyr),clf.decision_function(X_)))
				elif Y_ == 2:
					samsung.append((x, y, x+int(window_size[0]), y+int(window_size[1]),(ds**pyr),clf.decision_function(X_)))
		pyr += 1

	print "using nms to prune results..."
	samsung,apple = nms(samsung,apple,0.3)
	for p in samsung:
		cv2.rectangle(img, (int(p[0]*p[4]), int(p[1]*p[4])), (int(p[2]*p[4]), int(p[3]*p[4])), (0, 255, 0), thickness=5)
	for p in apple:
		cv2.rectangle(img, (int(p[0]*p[4]), int(p[1]*p[4])), (int(p[2]*p[4]), int(p[3]*p[4])), (255, 0, 0), thickness=5)
	cv2.imshow("Iphone in White, Samsung in Black", img)
	cv2.waitKey(0)

# Read the image
if __name__ == "__main__":
	cap = cv2.VideoCapture(0)

	ret,frame = cap.read()

	while ret:
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		cv2.imshow("webcam",frame)
		if cv2.waitKey(1) == 32:
			break
		ret,frame = cap.read()

	cap.release()
	cv2.destroyAllWindows()
	check_phone(frame)
