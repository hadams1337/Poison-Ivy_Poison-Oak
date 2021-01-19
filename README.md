# Poison-Ivy and Poison Oak Identification


I have a serious allergy to poison ivy and poison oak, but I don't know what poison ivy or poison oak look like.  I decided to build an app that would input a picture and output whether it was poison ivy, poison oak or a benign plant.

## Step 1 Data Collection
403 pictures of Poison Oak, 436 pictures of Poison Ivy were downloaded from google.  The pictures were picked by looking for pictures with a forest background and contained a mixture of spring, summer and fall plants. 2400 pictures of benign plants with leaves similar to poison ivy or poison oak were also downloaded from google.  The pics were chosen by hand to ensure that they did not contain poison ivy, were in a forest background, and had similarity to poison ivy with some notable difference. (eg. virginia creeper with 5 leaves, hog's peanut with a more rounded leaves, berries which have serrated leaves, etc.)

## Step 2 Modeling
### Quick and Dirty Start
I decided to use a simple convolutional neural network (CNN) to identify the plants.  I wanted to get a feel for the challenges in the dataset.  The results are shown below.
<p align="center">
  <img width="450" height="300" src=./graphs/simplemodel64.png>
</p>

The graphs show noisy traces for the loss and recall of the system, amplified in the validation set.  This shows that the decision landscape that the CNN is navigating is complicated.  That's not unsurprising, given that identifying plants from leaves with a natural (non-lab) background is a difficult task.
The other notable feature is the large gap between the training and validation loss.  The affect on recall is small, but in the loss it is significant.  This indicates overtraining and is unsurprising given the relatively small sample pool.
The classification results are shown below.  The number in the box is the percent of each true class (row) in each predicted class (column) (so each row will sum to 1.)
<p align="center">
  <img width="300" height="300" src=./graphs/simplemodel64_2.png>
</p>

The confusion matrix shows good recognition of benign plants (probably due to the imbalanced class) but it has a distinct tendency to classify poison ivy as benign.  This is the type of mistake I want to avoid.  My goal was to bring the % classification of poison ivy and poison oak as benign to under 20%.  I was willing to tolerate some loss in 
I decided to tackle the overtraining first because I didn't want to waste modeling power focusing on information that was only in the training set and wouldn't lead to better ID of unseen pictures.

### Image Augmentation
To decrease the ability of the CNN to focus on irrelevant information I increased image augmentation stepwise.  Zoom, tilt, reflection around a vertical axis, left/right and up/down shifts, and brightening were added to the pictures as they were added to the network. An example of the modifications is shown below.
<p align="center">
  <img width="300" height="300" src=./graphs/augmentation.png>
</p>
Each increase in the amount of augmentation that was successful lowered the gap between training and validation, which allowed me to add filters (increased stepwise from 32 to 128) and two extra layers.  Once I reached a plateau in ID where no overtrainin was present but modifications to the model wouldn't improve performance I retrained using the class weights feature in TensorFlow to impose artificial balance to the classes.
The final model confusion matrix is shown below.
<p align="center">
  <img width="300" height="300" src=./graphs/simplemodel128x2_2aug_zb_weights.png>
</p>
Increasing network complexity while increasing augmentation gave better, more certain results from the model.  Balancing the classes with weights has reduced the tendency of the CNN to call unknown plants benign, which reduced the correct predictions in the benign category, but the classification of the poison ivy had a dramatic improvement.  I still haven't hit less than 20%.

# Post-Model Result Modification
In my original model I was taking the result that has the highest certainty and assigning it, I decided to use any uncertainty in the model to apply a post-modeling modification to bias uncertain results toward being called poisonous.  I decided that I would subtract a fixed amount from the benign certainty and I found the optimal value for that by finding a local maximum for the combination of correct benign predictions, poison ivy predicted as toxic, and poison oak predicted as toxic. The best modification is shown by the golden vertical line on the graph below. 
<p align="center">
  <img width="300" height="300" src=./graphs/post_model_mods.png>
</p>
This produced the confusion matrix below.
<p align="center">
  <img width="300" height="300" src=./graphs/simplemodelwt_mod.png>
</p>
The final predictions exceeded requirements and maintained significant classification of benign plants as benign.