# Deep Learning for Medical Image

## Introduction

For this practice I trained six AI with the architecture of Unet. The parameters estudied for see if exists any improvements are Optimizer and Batchsize.

For test better and see if model has enought data I made a data augmentation rotating age image 90 and 180 degrees for see if exists any improvement with more data. An example is provided below. 

Original           |  Rotated 90 | Rotated 180
:-------------------------:|:-------------------------:|:-------------------------:
![](img_report\ISIC_0000000.jpg)  |  ![](img_report\ISIC_0000000_90.jpg) |  ![](img_report\ISIC_0000000_180.jpg)

Original           |  Rotated 90 | Rotated 180
:-------------------------:|:-------------------------:|:-------------------------:
![](img_report\ISIC_0000000_Segmentation.png)  |  ![](img_report\ISIC_0000000_90.png) |  ![](img_report\ISIC_0000000_180.png)

## Test and metrics

A differents tests was made. The results during the training can see on the following plots that are below. The plots show was de accuracy and the loss during the training. The diferent test executed was changing first the optimitzer. Two optimizers was tested, first RMSPROP and second Adam without data augmentation and the second test was changing the batchsize. 

### **RMSPROP Without Data Augmentation Batchsize 8**


Accuracy          |  Loss
:-------------------------:|:-------------------------:
![](report_img\8_bat_rmsprop_noDA_acc.png)  |  ![](report_img\8_bat_rmsprop_noDA_loss.png) 

### **Adam Without Data Augmentation Batchsize 8**


Accuracy          |  Loss
:-------------------------:|:-------------------------:
![](report_img\8_bat_adam_noDA_acc.png)  |  ![](report_img\8_bat_adam_noDA_loss.png) 

### **RMSPROP Without Data Augmentation Batchsize 16**

Accuracy          |  Loss
:-------------------------:|:-------------------------:
![](report_img\16_bat_rmsprop_noDA_acc.png)  |  ![](report_img\16_bat_rmsprop_noDA_loss.png) 



### **Adam Without Data Augmentation Batchsize 16**

Accuracy          |  Loss
:-------------------------:|:-------------------------:
![](report_img\16_bat_adam_no_da_acc.png)  |  ![](report_img\16_bat_adam_no_da_loss.png) 



### **RMSPROP Data Augmentation Batchsize 16**

Accuracy          |  Loss
:-------------------------:|:-------------------------:
![](report_img\16_bat_rmsprop_da_acc.png)  |  ![](report_img\16_bat_rmsprop_da_loss.png)



### **Adam Data Augmentation Batchsize 16**

Accuracy          |  Loss
:-------------------------:|:-------------------------:
![](report_img\16_bat_adam_da_acc.png)  |  ![](report_img\16_bat_adam_da_loss.png)


## Metrics

|Name                          |Sensitivity       |Specificity       |Accuracy          |jaccard           |dice_val          |
|------------------------------|------------------|------------------|------------------|------------------|------------------|
|adam_bat8_30_epoc_noDA.h5     |**0.873**|0.920|0.896|0.714|0.808|
|adam_bat16_30_epoc_DA.h5      |0.794|0.943|0.888|0.631|0.752|
|adam_bat16_30_epoc_noDA.h5    |0.828|0.960|0.912|0.724 |0.816|
|rmsprop_bat8_30_epoch_noDA.h5 |0.791|**0.974**|0.904|0.693|0.798|
|rmsprop_bat16_30_epoc_DA.h5   |0.731 |0.944|0.855|0.553|0.692|
|rmsprop_bat16_30_epoch_noDA.h5|0.870 |0.964|**0.926**|**0.764**|**0.849**|


According to these plots we can see how the accuracy in validation always starts in 1 and during the training this fal to 0.8-0.7. Meanwhile the accuracy in training is always stable. 

If we check the table that we have above we can observe different metrics. This metrics are from de test dataset once the model was trained. We can see that the best model  was trained with RMSPROP without data augmentation and batchsize 16. 

## Predictions of mask 

In the following plots it's possible to see how different models are doing the predictions and what is the result. 


**Adam batchsize 16 without data Augmentation**
![](report_img\adam_16_no_da.png)



**Adam batchsize 16 with data Augmentation**
![](report_img\16_bat_adam_da.png)


In this case we can see how models predicts better without data augmentation. The shape it's better without data augmentation. This can be appreciate it well on the last image.

**RMSPROP batchsize 16 without data Augmentation**
![](report_img\rmsprop_16_no_da.png)



**RMSPROP batchsize 16 with data Augmentation**
![](report_img\rmsprop_16_da.png)

Meanwhile with RMSPROP we can see how different models are doing a similar predictions (with and without data augmentation) but it occurs the same. Without data augmentation model learns better how to predict the mask. 

