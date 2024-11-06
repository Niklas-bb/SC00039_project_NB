# SC00039_project_NB
New project repo for python course with added license,

The purpose of this project is to make a python script that takes nd2 files from confocal microscope as input. Applies filter to the image to remove background noise and then count the number of nuclei.
The nuclei are stained with a flourescent marker called DAPI. The nuclei should have some distance from one another, which means it should work to count the number of nuclei.



## Data
The data to the the script is found in the folder called ICC_TEST_FOR_PYTHON. It contains the nd2 files called Figure1, FIgure2, Figure3. Each nd2 file contains 3 channels, but we will only focus on the first channel, channel0 since it contains the DAPI.

## Packages needed for the script
```bash
import argparse
import os
import numpy as np
import matplotlib.pyplot as plt
import nd2
from skimage.filters import gaussian, threshold_otsu
from skimage.measure import label, regionprops_table
from skimage.segmentation import clear_border
from skimage.morphology import area_opening
import pandas as pd
```

## How to run the script
### Download the folder from github
Download the project files to your computer. You can do this by cloning the repository or downloading it as a zip file.
```bash
git clone https://github.com/Niklas-bb/SC00039_project_NB.git
```
## Activate the environment
I used miniconda3 to run script. DOwnload if you do not already have.

## Environment Setup
Conda environment is used. The provided environment.yml should include all packages required.

### Step 1: To create the environment that will be used to install Jupyter Lab.
```bash
conda create -y -n dapicount-env -c conda-forge python=3.9
```
### Step 2: Activate environment
Activate the environment named Dapicount environment:

```bash
conda activate Dapicount
```

## Running the code 
I run the code using the following command in Git bash:
```bash
python DAPIcountfinal.py --folder "C:\path\to\your\nd2\files"
```
In my case the command to run the script is: 
```bash
python DAPIcountfinal.py --folder "C:\Users\Niklas\OneDrive\Dokument\Sahlgrenska\Courses\python_for_biologists_SC00039\SC00039_project_NB\ICC_TEST_FOR_PYTHON"
```
But make sure you change the path to your folder. 





### Output
The output from the script is a number of images of the different stages of filtering steps. As the script is now you will get 3 images for each nd2 file. You can uncomment some lines in the python scipt to see more images of filtering stages.
There is also an histogram of the sizes of the nuclei and then a table showing for example the nuclei count, area and mean instensity.

