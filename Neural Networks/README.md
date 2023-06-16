## 1. Overview

Stored as pickle files, each of the batch files contains a dictionary with the following elements:

- data -- a 60000x784 numpy array of uint8s. Each row of the array stores a 28x28 gray scale image

- labels -- a list of 60000 numbers in the range 0-9. The number at index i indicates the label of the ith image in the array data.

The dataset contains another file, called dataset.meta. It too contains a Python dictionary object. It has the following entries:

- label_names -- a 10-element list which gives meaningful names to the numeric labels in the labels array described above. For example, label_names[0] == "T-shirt/top", label_names[1] == "Trouser", etc.

## 2. Data Split

You can choose how you go about splitting the data, as long as it's done appropriately.
