import cv2
import argparse
import imutils
import sys
import os

parser = argparse.ArgumentParser(description='Given image, creates set of angles, and pyramids')
parser.add_argument('i', help='the image')

args = parser.parse_args()

#creates pyramids
def get_py(img,levels):
    imgs = []
    imgs.append(img)
    for i in range(levels-1):
        imgs.append(cv2.pyrDown(imgs[i]))
    return imgs

def get_rot(img):
    imgs = []
    imgs.append(img)
    for i in range(45,360,45):
        imgs.append(imutils.rotate_bound(img, i))
    for i in range(len(imgs)):
        imgs[i] = get_py(imgs[i],3)
    return imgs

img = cv2.imread(args.i)

imgs = get_rot(img)

d = args.i.split('.')[0]

if not os.path.exists(d):
    os.makedirs(d)
else:
	print 'Folder already exists'
	sys.exit(0)

for i in range(len(imgs)):
	for j in range(len(imgs[0])):
		cv2.imwrite(d + '/' + d + '-' + str(i) + '-' + str(j) + '.jpg',imgs[i][j])