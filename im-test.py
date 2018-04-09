import webcam2
import cv2
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='given test image returns results')
	parser.add_argument('tim', help='the test image')
	args = parser.parse_args()

	img = cv2.imread(args.tim,0)
	webcam2.check_phone(img)