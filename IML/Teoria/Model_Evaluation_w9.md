# Theory 9. Model Evaluation



Why do we evaluate a model's performance?

* To know how well it works, reporting results etc...
* To compare models. For choose which model is better. 

## Definition

* **Model Evaluation** is the process of assessing a property or properties of a model
  * Evaluation metrics
  * Evaluation techniques
* **Model Selection** is the process of choosing among many candidate models for a predictive modeling problem. 
  * Probabilistic measures
  * Resampling methods

In model evaluation:

* A learning algorithm must interpolate appropriate predictions of regions of the instance space that are not included in the training data.
* Algorithm evaluation techniques are designed to provide more reliable estimates of the accuracy of the models learning by an algorithm than would be obtained by assessing them on the training data. 

## Evaluation metrics

### Performance metrics

* Precision & Recall & F1 score

  * Precision: What percent of our predictions are accurate?

  * Recall: How many of the accurate predictions did we capture

  * F1 score: Single number that combines the two values. Good for ranking / sorting
    $$
    \text{F1} = 2 \times\frac{precision \times recall}{precision + recall}
    $$
    

* Precision at N

  * How many accurate examples did we capture in our top N ranked examples. This is often used in information (document) retrieval

### Confusion matrix

![]()