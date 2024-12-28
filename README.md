#◢ Colorize your own photos!

####**Project Description:**
Transform black-and-white images into beautifully colored images using Deep Learning. This project employs advanced techniques to predict colors and produce vibrant, realistic results.

####Original paper: [Colorful Image Colorization](https://arxiv.org/pdf/1603.08511)

####**How It Works:**
All images are converted from the RGB color space to the Lab color space, which is more suitable for colorization tasks.

####**Lab Color Space Overview:**
L channel: Encodes lightness intensity only.

a channel: Encodes green-red colors.

b channel: Encodes blue-yellow colors.

###Using this space, the process works as follows:

The L channel is extracted from the grayscale input image and fed into the network.

The network predicts the a and b channels.

The predicted ab channels are combined with the original L channel to reconstruct the final colorized image.

###Technologies and Tools:
Python

Deep Learning (for model training and predictions)

OpenCV 3.4.2+ (for image preprocessing and visualization)

Numpy (for numerical computations)
