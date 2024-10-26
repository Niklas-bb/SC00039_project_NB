#!/usr/bin/env python
# coding: utf-8

# # The purpose of this script is count number of nuclei from nd2 files
# Note that the script will output images of all steps, original image, before during and after filter steps.
# This is to see what every step does to the image. There are total 18 images (6 for each nd2 file).
# To see the next image the one that is currenly opened should be closed. 
# ### Nuclei from neurons are stained with DAPI and then imaged with confocal images

# In[1]:


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

# Function to load and process ND2 files
def process_nd2_file(file_path):
    with nd2.ND2File(file_path) as figure:
        image = figure.asarray()
        print(f"File path: {figure.path}")
        print(f"File shape: {figure.shape}")

        # Assuming DAPI is in channel 0
        ch0 = image[0, :, :].squeeze()

        # Original Image
        plt.figure(figsize=(4, 4), dpi=300)
        plt.imshow(ch0, cmap='gray')
        plt.title(f'Original DAPI from {os.path.basename(file_path)}')
        plt.axis('off')
        plt.show()

        # Apply Gaussian filter
        #NOTE: if you uncomment row 44-48 images of this step will be shown
        img_bg = gaussian(ch0, sigma=50, preserve_range=True)
        #plt.figure(figsize=(4, 4), dpi=300)
        #plt.imshow(img_bg, cmap=plt.cm.gray)
        #plt.title(f'Background (Gaussian) from {os.path.basename(file_path)}')
        #plt.axis('off')
        #plt.show()

        # Remove background
         #NOTE: if you uncomment row 54-58 images of this step will be shown

        img_no_bg = ch0 - img_bg
        #plt.figure(figsize=(4, 4), dpi=300)
        #plt.imshow(img_no_bg, cmap='gray')
        #plt.title(f'Background Removed from {os.path.basename(file_path)}')
        #plt.axis('off')
        #plt.show()

        # Otsu's thresholding
        th_val = threshold_otsu(img_no_bg)
        print(f'Otsu threshold value: {th_val}')
        bw_otsu = img_no_bg > th_val

        # After thresholding
        #NOTE: if you uncomment row 67-71 images of this step will be shown
        #plt.figure(figsize=(4, 4), dpi=300)
        #plt.imshow(bw_otsu, cmap='gray')
        #plt.title(f'Otsu Segmentation from {os.path.basename(file_path)}')
        #plt.axis('off')
        #plt.show()

        # Clear border and remove small objects
        mask = clear_border(bw_otsu)
        mask = area_opening(mask, area_threshold=200)

        # Connected component analysis
        lbl = label(mask)
        plt.figure(figsize=(4, 4), dpi=300)
        plt.imshow(lbl)
        plt.title(f'Connected Components from {os.path.basename(file_path)}')
        plt.axis('off')
        plt.show()

        # Extract region properties
        properties = ['label', 'area', 'eccentricity', 'mean_intensity']
        table = regionprops_table(label_image=lbl, intensity_image=ch0, properties=properties)
        table = pd.DataFrame(table)

        print(table.head())
        print(table.describe())

        # Histogram of areas
        table.hist(column='area', figsize=(4, 4))
        plt.show()

# Command-line argument parsing
def main():
    parser = argparse.ArgumentParser(description="Process ND2 files and perform DAPI counting.")
    parser.add_argument(
        '-f', '--folder', 
        type=str, 
        required=True, 
        help="Path to the folder containing ND2 files."
    )
    args = parser.parse_args()

    # Retrieve file names from the provided folder
    folder_path = args.folder
    file_names = [f for f in os.listdir(folder_path) if f.endswith('.nd2')]

    if not file_names:
        print(f"No ND2 files found in the folder: {folder_path}")
        return

    # Process each ND2 file
    for file_name in file_names:
        file_path = os.path.join(folder_path, file_name)
        process_nd2_file(file_path)

if __name__ == "__main__":
    main()

