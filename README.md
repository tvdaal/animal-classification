# Description
In this repository I build and train a convolutional neural network (CNN) in Keras to classify [Big Five](https://en.wikipedia.org/wiki/Big_five_game) animals from images. The images are obtained through web scraping and resized (respecting the aspect ratio) to a target resolution of 400 x 400 pixels. To increase the number of images during training, data augmentation is applied. Different regularization settings are tested.

I decided to build this model for fun and to explore web scraping and certain Keras features. I chose this dataset because I have a passion for animals and am fortunate enough to have seen the Big Five in the wild in Tanzania.

# Installation
This repository requires Python 3. To get started, run the following commands:

```
git clone https://github.com/tvdaal/animal-classification.git
cd animal-classification
conda env create -f environment.yml
conda activate py39-animals
python -m ipykernel install --user --name py39-animals --display-name "py39-animals"
```

The virtual conda environment called 'py39-animals' contains all necessary packages and dependencies. The last step ensures that the IPython kernel uses the right environment.
