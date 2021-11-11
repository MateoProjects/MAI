# Visualization

**Objective:** Visualizing low-dimensional views of high-dimensional data

Main goal is to communicate the information clearly and effectively through graphical means. So the **VISUALIZATION** is the study of the visual representation of the data. 

Information  > data > knowledge > wisdom

![](img/w5/lego-connect.png)

**How do we visualize data of high dimensionality?**

* Eliminate dimensions
* Dive & conquer: create multiple visualizations of low dimensionality
* Latent and projection models

## Latency and projection

**Projection**

* Dimensionality compression
* Similitude information coding

**Clustering**

* Finding grouping structure in data
* Similitude information coding

**Self-Organizing Map(SOM) & Generative Topographic Mapping (GTM)**

* Combine latent representation and clustering

## Self Organizing Maps

**Applications**

* Clustering
* Visualization
* Dimensionality reduction
* Classification
* Feature extraction

The purpose of SOM is to map a multi-dimensional input space onto a topology preserving map of neurons

*  Preserve a topological so that neighboring neurons respond to «similar» input patterns
* The topological structure is often a 2 or 3 dimensional space

![](img/w5/som.png)

### Commonly output-layer structures

![](img/w5/som_dim.png)

* SOM maps a multi-dimensional input space onto a topology preserving map of neurons

* Each neuron is assigned a weight vector with the same dimensionality of the input space

* Each Input pattern is compared to each weight vector
* Distance is calculated between the input pattern and each neuron in the network (e.g. Euclidean Distance)
* Selects the neuron that is closest as the winning neuron

### Adaptation in SOM

* During training, the “winner” neuron and its neighborhood adapts to make their weight vector more similar to the input pattern that caused the activation.
* The neurons are moved closer to the input pattern.
* The magnitude of the adaptation is controlled via a learning parameter which decays over time.

![](img/w5/adaptation_som.png)

### Topological error

* Evaluates the complexity of the output space
* Measures the number of times the secund closest neighbor in the input space is not mapped into the neighbourhood of the neuron in the output space.
* A hight topolofical error may indicate that the classification problem is complex or may suggest that the training was not adequate and the network is folded. 

### SOM training process 

* Neurons initialized ramdomly
* Unfolding phase
  * Neurons are "spread out" and pulled towards the general area (in the input space) where they will stay
* Fine tuning phase
  * SOM match the neurons as far as possible to the input patterns, thus decreasing the quantization error

## Multi-Dimensional Scaling (MDS)

The goal of an MDS analysis is to find a spatial configuration of objects when all that is known is some measure of their general (dis)similarity. 

Reduces large amounts of data into easy-to-visualize structures

How? By assigning instances to specific locations in space

Distances between points in space match dis/similarities as closely as possible: 

* Similar objects: Close points
* Dissimilar objects: Far apart points