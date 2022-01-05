# TEMPLATES HOG

Eye-trackers applications

* Market research
* Usability research
* Packaging research

## Template matching

![](img/w4/template matching.png)

First Method : SSD

![](img/w4/ssd.png)

Second method: Normalized cross-correlation

![](img/w4/normalized_cross_correlation.png)

![](img/w4/normalized_cross_correlation2.png)

Third method: Convolutional filtering the normalized image. 

![](img/w4/method3.jpg)

![](img/w4/template matching.jpg)

## Image descriptors

To solve real world problems (image retrieval, image classification, etc.), we need to find a connection between:

* a matrix of pixels (raw representation),
* what humans see in an image (face, smile, emoticon).

Image descriptors allow to describe and represent the image/object by quantities (colour, shape, regions, textures and motion) closer to the visual characteristics perceived by humans.

### Histogram of gradient (HOG)

![](img/w4/hog.png)

• The image gradient at each pixel is a vector. 

• As a vector, it has a magnitude and a direction. 

![](img/w4/hog2.png)

Remember histogram of colour images

![](img/w4/gradient_colour_images.jpg)

Histogram of gradient orientations

![](img/w4/hog3.png)

* Te gradient orientation is an angle
* Count occurences of gradient orientation in a patch
* Quantize to 8 bins, each bins cover 45 degrees
* Visual representation of the histogram

![](img/w4/histogram_bins.jpg)

We will divide the image in to a small connected regions called cells.

Compute local histogram for each cell

Simply concatenate the histogram of the cells.

![](img/w4/hog4.png)

![](img/w4/hog5.png)

For compute gradient in practice we convolve the image with discrete derivative mask:

Dx=[-1, 0, 1], Dy=[1, 0, -1] T

## Pedestrian detection

Transform the detection problem into a binary (yes/not) classification problem.

Compute HOG descriptor for all training samples

![](img/w4/hog6.png)

Descriptor extraction: 

(a) Get the average gradient image over query and test examples, 

(b) Extract HOGs for the query image,

(c) Extract HOGs for the dataset of images.

HOG-based Retrieval: 

(d) For each dataset image, extract the region bottom left and compare to the query HOG. 

(e) Apply the sliding window technique all over the image and compute the HOGs correlation 

(f) Apply the maximum over the correlation resulting image. 

(g) Decide if the correlation is high enough -> Pedestrian vs. No-pedestrian

## Image Retrieval

Definition: Given an image (query image), the image retrieval consists of sorting the rest of images according to the similarity to the query image.

### Problem 1

How can we measure difference between both images: "building " and "nature"? 

![](img/w4/image_description_problem.jpg)

### Problem 2

Image retrieval definition: : Given an image (query image), the image retrieval consists of sorting the rest of images according to the similarity to the query image.

**Algorithm**

1. Define the image descriptor
2. Extract the image descriptors of the database images
3. Given a query image, extract its descriptor.
4. Sort the database images according to the similarity with the query image. 

The descriptor (or feature vector) should describe the image in a way that is invariant to all the image changes that are suitable to our application (e.g. color, illumination, noise etc.)

![](img/w4/image_descriptor.jpg)

### K-Nearest Neighbors for retrieval

The query is an unlabelled vector in our feature space.

Retrieve the k-closest neighbours as the relevant items to a query.

![](img/w4/image_descriptors_knn.jpg)

Training: 

1. Define image descriptors 
2. Use training set to extract their descriptors
3. Train a model 

***Note**: Represent each image of the training set by its descriptor. Store the descriptors and class labels of the training samples (labelled images)*.

Test: 

	4. Given a test example extract its descriptor 
	4. Apply the model and compare with the training examples to decide its label

***Note**: Compute the HOG –based descriptor of the test image. Apply the model/classifier to compare the descriptor of the test image to the descriptors of the training images in order to determine its class membership.*

![](img/w4/summary.jpg)

