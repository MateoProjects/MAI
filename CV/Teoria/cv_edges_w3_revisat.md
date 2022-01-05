# COMPUTATIONAL VISION: EDGES

## Edge detection

**Goal**: map image from 2d array of pixels to a set of curves or line segments or contours.

![](img/w3/edges_1.png)

We can detect edge when we have a change of intensity. 

## Derivatives and edges

An edge is a place of rapid change in the image intensity function.

![](img/w3/derivate_edge.png)

If image is a discrete matrix we can approximate it using finite differences. 

![](img/w3/finite_dif.jpg)

We need to use a partial derivatives.

![](img/w3/derivate_edge2.png)

When we have noise we can get the average of the three derivatives in order to be less sensitive to noise

![](img/w3/threederiv.jpg)

Filters:

![](img/w3/sobel.jpg)

The difference is that Sobel use non-uniform weights so gives more importance to the closest neighbors.

## Image gradient

![Test](img/w3/gradient.png)

The edge strength is given by the gradient magnitude

![](img/w3/gradient2.png)

Second derivatives: Given an edge, the first derivative has an extreme, and the second one has a zerocrossing in the edge and extremes before and after the edge.



**Discrete operators: Laplacian Mask**

![](img/w3/laplacian_mask.jpg)

## Mask properties Quiz

Test on smoothing

* Values should be _ _ _ _ _ _ _ 
* Sum to _ _ _ _ _ _  &rarr; constant regions same as input.
* Amount of smoothing _ _ _ _ _ _ _ _ _ to mask size.
* Remove “_ _ _ _ _  -frequency” components; “_ _ _ _ _ -pass” filter.

Test on derivatives

* _ signs used to get high response in regions of high contrast.

* Sum to _ &rarr; no response in constant regions.
* _  value at points of high contrast.

## Effects of noise



![](img/w3/noise.png)

**Solution**: Smoot first

![](img/w3/smooth_first.jpg)

### 2D edge detection filters

![](img/w3/2d_edge_detection_filters.jpg)

Parameter σ i is the scale / witth of the gaussian kernel and controls the amount of smoothing. 

![](img/w1/panda.jpg)

![](img/w3/pandas.jpg)

Larger values: high scale edges detected.

Smaller values: more features detected.



## Canny edge detector

Filter image with derivative of Gaussian.

Find magnitude and orientation of gradient.

Define two thresholds (hysteresis): low and high. Use the high threshold to start edge curves and the low threshold to continue them. 

### Non-maximum suppression

Check if pixel is local maximum along gradient direction, select single max across width of the edge. 

![](img/w3/non-maximum-supression.jpg)

![](img/w3/problem-non-maximum-supr.jpg)

### Hysteresis thresholding

Use a high threshold to start edge curves, and a low threshold to continue them.

![](img/w3/hysteresis.jpg)

**Example**

![](img/w3/example_hysteresis.jpg)

### Limitations of canny edge detector

Only focuses on local changes and it has no semantic understanding. 

![](img/w3/canny_edge_fail.jpg)

## Hybrid Images

Low frequencies &rarr; pixel values that are changing slowly over space.

High frequency &rarr; pixel values that are rapidly changing in space. 

![](img/w3/hybrid images.jpg)

## Summary

Filters allow local image neighborhood to influence our description and features.

* Smoothing to reduce noise
* Derivatives to locate contrast, high image gradient

Different edge detectors:

* Sobel & Prewitt – fast but sensitive to noise
* Convolution with the Gradient of a Gaussian
  * Less fast but more robust
  * Using different sigma allows to smooth more or less
  * Zero-crossing with a Laplacian – assures closed contours.
* Canny edge detector – state of the art edge detector
  * Assures continuous and thin contours due to the hysteresis and the thinning steps but needs parameters.
  * Edges used to contain good contours but also many other pixels with high intensity change.
