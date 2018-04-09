import cv2
import numpy as np 
import sys
import os
import argparse
from sklearn.externals import joblib
from skimage.feature import hog
from skimage.io import imread

parser = argparse.ArgumentParser(description='Given set of test images, allows user to select correct angle, and correct phone')
parser.add_argument('p1', help='the folder of first positive class')
parser.add_argument('p2', help='the folder of the second positive class')
parser.add_argument('n', help='the folder of negative images')
args = parser.parse_args()

'''
compute hog of all phones
compute hog of backgrounds (negatives)
save features to text documents
images were too large so I'm downsizing by 0.25
'''

aNames = os.listdir(args.p1)
i = 0
for p in aNames:
	if not p.endswith(".txt"):
		print 'img ' + str(i)
		img = cv2.imread(args.p1 + '/' + p,0)
		img = cv2.resize(img,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
		h = hog(img, 9, [8,8], [3,3])
		joblib.dump(h,args.p1 + '/' + p.split('.')[0] + '.txt')
		print len(h)
		i += 1

print 'done positive 1'

sNames = os.listdir(args.p2)
i = 0
for p in sNames:
	if not p.endswith(".txt"):
		print 'img ' + str(i)
		img = cv2.imread(args.p2 + '/' + p,0)
		img = cv2.resize(img,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
		h = hog(img, 9, [8,8], [3,3])
		joblib.dump(h,args.p2 + '/' + p.split('.')[0] + '.txt')
		print len(h)
		i += 1

print 'done positive 2'

nNames = os.listdir(args.n)
i = 0
for n in nNames:
	if not n.endswith(".txt"):
		print 'img ' + str(i)
		img = cv2.imread(args.n + '/' + n,0)
		img = cv2.resize(img,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
		h = hog(img, 9, [8,8], [3,3])
		joblib.dump(h,args.n + '/' + n.split('.')[0] + '.txt')
		print len(h)
		i += 1

print 'done negative'