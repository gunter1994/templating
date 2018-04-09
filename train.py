from sklearn import svm
from sklearn.externals import joblib
from skimage.feature import hog
from skimage.io import imread
import argparse
import numpy as np
import os

parser = argparse.ArgumentParser(description='Given set of test images, allows user to select correct angle, and correct phone')
parser.add_argument('p1', help='the folder of first positive class')
parser.add_argument('p2', help='the folder of the second positive class')
parser.add_argument('n', help='the folder of negative images')
args = parser.parse_args()

X = []
y = []

print 'loading class 1...'
for p in os.listdir(args.p1):
	if p.endswith(".txt"):
		xs = joblib.load(args.p1 + '/' + p)
		X.append(xs)
		y.append(1)

print 'loading class 2...'
for p in os.listdir(args.p2):
	if p.endswith(".txt"):
		xs = joblib.load(args.p2 + '/' + p)
		X.append(xs)
		y.append(2)

print 'loading negatives...'
for p in os.listdir(args.n):
	if p.endswith(".txt"):
		xs = joblib.load(args.n + '/' + p)
		X.append(xs)
		y.append(0)

print 'fitting...'
clf = svm.SVC(kernel='linear',decision_function_shape='ovr')

clf.fit(X, y)

print(clf.predict(X[0:20]))

joblib.dump(clf, 'model.pkl')