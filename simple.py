import cv2
import numpy as np
import argparse
import imutils
import matplotlib.pyplot as plt
import os

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

def get_score(tmpts,tests):
	mv = 0
	mtmp = [0,0]
	mtest = 0
	ml = [0,0]
	for ts in range(len(tmpts)):
		for t in range(len(tmpts[ts])):
			for test in range(len(tests)):
				if (tmpts[ts][t].shape[0] > tests[test].shape[0] or tmpts[ts][t].shape[1] > tests[test].shape[1]):
					continue
				res = cv2.matchTemplate(tests[test],tmpts[ts][t],cv2.TM_CCOEFF_NORMED)

				min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
				if max_val > mv:
					mv = max_val
					mtmp = [ts,t]
					mtest = test
					ml = max_loc
	return mv,mtmp,mtest,max_loc

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Given set of test images, allows user to select correct angle, and correct phone')
	parser.add_argument('tim', help='the folder of test images')
	args = parser.parse_args()

	test = cv2.imread(args.tim,0)
	testP = get_py(test,3)
	pNames = os.listdir('phones')
	phones = []
	for p in pNames:
		temp  = cv2.imread('phones/' + p,0)
		phones.append(get_rot(temp))

	mvs = []
	mtmps = []
	mtests = []
	mlocs = []
	for p in phones:
		mv,mtmp,mtest,ml = get_score(p,testP)
		mvs.append(mv)
		mtmps.append(mtmp)
		mtests.append(mtest)
		mlocs.append(ml)


	if mvs[0] == max(mvs):
		c = 'the back of a A5'
		ml = mlocs[0]
		tem = phones[0][mtmps[0][0]][mtmps[0][1]]
		img = mtests[0]
	elif mvs[1] == max(mvs):
		c = 'the front of a A5'
		ml = mlocs[1]
		tem = phones[1][mtmps[1][0]][mtmps[1][1]]
		img = mtests[1]
	elif mvs[2] == max(mvs):
		c = 'the back of an Iphone 8'
		ml = mlocs[2]
		tem = phones[2][mtmps[2][0]][mtmps[2][1]]
		img = mtests[2]
	elif mvs[3] == max(mvs):
		c = 'the front of an Iphone 8'
		ml = mlocs[3]
		tem = phones[3][mtmps[3][0]][mtmps[3][1]]
		img = mtests[3]
	elif mvs[4] == max(mvs):
		c = 'the back of a S8'
		ml = mlocs[4]
		tem = phones[4][mtmps[4][0]][mtmps[4][1]]
		img = mtests[4]
	elif mvs[5] == max(mvs):
		c = 'the front of a S8'
		ml = mlocs[5]
		tem = phones[5][mtmps[5][0]][mtmps[5][1]]
		img = mtests[5]

	print mvs
	print "The phone is " + c

	w, h = tem.shape[::-1]
	bottom_right = (ml[0] + w, ml[1] + h)

	cv2.rectangle(testP[img],ml, bottom_right, 0, 5)

	plt.imshow(testP[img],cmap = 'gray')
	plt.title('Test Image'), plt.xticks([]), plt.yticks([])
	plt.show()