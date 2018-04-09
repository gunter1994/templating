## templating

# Methods

2 different methods are at use here in this project, first off the simple templating method using TM_CCOEFF_NORMED, and the second one using HOG and SVM.

# CCOEFF TEMPLATING

my files involved in templating is the ipnb "final" which I used for all my initial testing. I didn't get very good results so I decided to try somme harder methods.

Most of this is unfinished as I quickly realised this method was getting no where near the results I wanted, I did get a webcam test working, but it never recognized any phones properly and just randomely guessed at the background.

# HOG and SVM

The idea behind my HOG SVM classifier was to classify if a phone was the iphone brand or the samsung brand. I have several pictures of both from the back (from the front had too many issues due to the screen). As well as several random pictures I downloaded online that are simply "not phones". 

Using hog.py it will generate a text file for every image with the corresponding HOG feature information.

Now with this information we can try to train a SVM, this is where train.py comes in. Using train.py it will automatically read all of the .txt feature files, and set up a network to classify using a linear SVM. I tried other models of SVM but linear seems to be by far the most effective.

This SVM model is than saved to a pkl file.

This finally brings us to the testing stage. The two tests you can use are webcam2.py and im-test.py. Webcam2.py builds off my earlier test, allowing you to press space to take an image, and have the algorithm try to find any phones in it.

I did not have much success with this, although there weren't really any false positives it just didn't work very well, but I also have a very low quality webcam, and the algorithm seems to work better on larger images.

The second test is im-test.py which simply lets you run the algorithm on a given images using the pre trained model I've included (which you can overwrite if you want.

Some of my results can be seen below.

![Iphone example](../master/examples/Figure_1.png)
![Samsung example](../master/examples/Figure_2.png)
