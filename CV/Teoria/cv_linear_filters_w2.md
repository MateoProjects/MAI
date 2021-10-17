# Computational vision : Linear Filters

### Digital Images

Try to think of images as a matrices taken from a sensor array

![](img/w2/simi_1.JPG)

* Sample the 2D space on a regular grid

* Quantize each sample (round to nearest integer)

  

![](img/w2/grid.JPG)

## How do we obtain color images?

Light is an energy source that carries coded information about the world which can be read from a distance through the images.

A human eye will respond to wavelengths from about 380 to 750 nm.

## Images in Skimage

Image can be Grey-value (1 channel) or color images (3 channels)

![](img/w2/grid2.JPG)

## Spatial resolution

* **Sensor resolution**: size of real world scene element that images to a single pixel
* **Image resolution**: number of pixels

## Image Magnification

![](img/w2/magnification.JPG)

## Image reduction

![](img/w2/reduction.JPG)

## Photometric resolution

![](img/w2/photometric.JPG)

Histogram of an image represents the frequencies of the image grey levels.

## Histogram manipulation for contrast enhancement

To increase the contrast we need to apply the following:

![](img/w2/contrast.JPG)

**Example**

![](img/w2/contrast2.JPG)

## How to process by a lineal filter

### Image Filtering

**Linear Filtering**: Compute a function of the local neighborhood at each pixel in the image.

* Function specified by a filter or mask saying how to combine values from neighbors.

### Common types of noise

* Salt and pepper noise: random occurrences of black and white pixels.
* Impulse noise: random occurrences of white pixels
* Gaussian noise: variations in intensity drawn from a Gaussian normal distribution
* ![](img/w2/types_of_noise.JPG)

### Reducing Noise

* Firs attempt at a solution:
  * Replace each pixel with an average of all the values in its neighborhood
  * Assumptions:
    * Expect pixels to be like their neighbors
    * Expect noise processes to be independent from pixel to pixel

![](img/w2/smooth1.JPG)

For each pixel i, multiply its neighborhood by a mask:

![](img/w2/smooth2.JPG)

### Weighted Moving Average

to do

### Moving Average in 2D

to do

### Convolutional filtering

Say the averaging windows size is (2k + 1) x (2k +1):

![](img/w2/conv_filtering.JPG)

And for Non-uniform weights

![](img/w2/conv_filtering_no_uniform.JPG)

### Properties of convolution

* Shift invariant:

  * Operator behaves the same everywhere, i.e. the value of the output depends on the pattern in the image neighborhood, not the position of the neighborhood.

* Superposition:
  $$
  h * (f1 + f2) = (h * f1) + (h * f2)
  $$
  

## Mean and median filters

![](img/w2/median_filter.JPG)

Median filter is edge preserving

![](img/w2/median_vs_mean.JPG)

## Linear filters with Gaussians

2D Gaussian function
$$
h(u,v) = \frac{1}{2\pi\sigma^2}e^{-\frac{u^2 + v^2}{\sigma^2}}
$$
![](img/w2/gausian.JPG)

![](img/w2/size_kernels.JPG)

• Variance of Gaussian: determines extent of smoothing

![](img/w2/gaussian2.JPG)

