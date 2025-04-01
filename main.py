'''
This is the main code to run analysis on data extracted from SLEAP.
If you are using this project, I recommend setting it in the same environment as SLEAP so
you don´t have to re-download the packages that are required for analysis.
Some scripts were used from the website sleap.ai: https://sleap.ai/notebooks/Analysis_examples.html
'''
import h5py
import numpy as np
import os
import pandas as pd
from functions import fill_missing, select_label, smooth_diff, corr_roll, reading_h5files
from visualizations import plot_tracks, plot_velocity, plot_velocity2d


#1. UPLOAD DATA #for now I am using one file then it will be a loop
filepath = '/mnt/datafast/vanesa/SLEAP_projects/analysis/'
filemetadata = '/mnt/datafast/vanesa/SLEAP_projects/analysis/metadata_demo.xlsx'
df_metadata = pd.read_excel(filemetadata)#upload metadata as df
# Loop through all files in the directory
for file in os.listdir(filepath):
  filename, dset_names, locations, node_names, video_name = reading_h5files(file, filepath)

    #2.1. FILL MISSING VALUES
  locations = fill_missing(locations)  #interpolate when a label wasn't detected e.g. hidden by environment

    #2.1.A LABEL OF CHOICE ACROSS VIDEO FOR BOTH ANIMALS
  selected_index, selected_label = select_label(node_names) #define labels index and location
  label_loc = locations[:, selected_index, :, :] #extract locations of the selected label
  plot_tracks(video_name,label_loc, selected_label) #plot the tracks of both animals for the same selected label

    #3. MEASURES
    #3.1. VELOCITY FOR ONE ANIMAL (track is an animal)
  track = 0 #choose the animal- It can be track 0 or track 1. #FIXME change to dialog in the future
  track_name = 'track'+ str(track)
  label_vel_track = smooth_diff(label_loc[:, :, track])
  plot_velocity(label_loc,label_vel_track, video_name, selected_label, track_name)
  plot_velocity2d(label_loc,label_vel_track, video_name, selected_label,track_name)

  label_vel_track0 = smooth_diff(label_loc[:, :, 0])
  label_vel_track1 = smooth_diff(label_loc[:, :, 1])

  # 4.1. TRAVELLED DISTANCE - GOAL FOR LAB MEETING
  '''
    when we calculated velocity we calculated displacement per frame. 
    How many pixels per frame the rat moved. To calculate the travelled distance we can sum
    the total displacement across all frames.
    '''
    # I am going to calculate for track 0 then track 1. Maybe I do a loop later when I am refining the code we'll see.
  label_td_track0 = np.sum(label_vel_track0, axis=None, dtype=None, out=None)  # total travelled distance in pixels
  label_td_track1 = np.sum(label_vel_track1, axis=None, dtype=None, out=None)

    #3.3.COVARIANCE OF VELOCITY BETWEEN TWO ANIMALS
  win = 300
  label_vel_track0 = smooth_diff(label_loc[:, :, 0])
  label_vel_track1 = smooth_diff(label_loc[:, :, 1])
  cov_vel = corr_roll(label_vel_track0, label_vel_track1,win) #FIXME

tk =2
#brainstorm of measures of interest
#4.2. TIME IN CLOSED PROXIMITY

#4.3. TIME LABEL A IN TRACK-0 WAS CLOSED TO LABEL B IN TRACK-1
