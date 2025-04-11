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
from functions import fill_missing, select_label, smooth_diff, corr_roll, reading_h5files, rowmatch
from visualizations import plot_tracks, plot_velocity


#1. UPLOAD DATA #for now I am using one file then it will be a loop
filepath = '/mnt/datafast/vanesa/SLEAP_projects/analysis/e1/'
filemetadata = '/mnt/datafast/vanesa/SLEAP_projects/analysis/e1/metadata_e1.xlsx'
df_metadata = pd.read_excel(filemetadata)#upload metadata as df
resultsfolder = filepath + 'Results/' #path for results

# Loop through all files in the directory
for file in os.listdir(filepath):
  if not file.endswith(".h5"):
    pass
  else:
   filename, dset_names, locations, node_names, video_name, track_tags = reading_h5files(file, filepath)
   print(filename)
   fileresults = resultsfolder + video_name +'/'
   os.makedirs(fileresults, exist_ok=True) #videoresults
     #2.1. FILL MISSING VALUES
   #TODO maybe I add a filter for score >0.9 (individual label score)
   locations = fill_missing(locations)  #interpolate when a label wasn't detected e.g. hidden by environment

     #2.1.A LABEL OF CHOICE ACROSS VIDEO FOR BOTH ANIMALS - CHOOSE ONLY AT THE BEGINNING
   if 'selected_label' not in globals() and 'selected_label' not in locals():
    selected_index, selected_label = select_label(node_names) #define labels index and location

   label_loc = locations[:, selected_index, :, :] #extract locations of the selected label
   plot_tracks(video_name,label_loc, selected_label,track_tags, fileresults) #plot the tracks of both animals for the same selected label

     #3. MEASURES PER ANIMAL (loop)
     #3.1. VELOCITY
   label_vel_tracks = {} # Dictionary to store velocity for each track
   rowtrack = rowmatch(df_metadata, video_name, track_tags)  # function to name the tracks
   # Loop over the tracks (0 and 1)
   for track in track_tags:
     track_index = track_tags.index(track)
     label_vel_tracks[track] = smooth_diff(label_loc[:, :, track_index]) # Extract the velocity variable for the current track
     plot_velocity(label_loc, label_vel_tracks[track], video_name, selected_label, track, track_index, fileresults) # Plot using the first plot function
   # 3.2. TRAVELLED DISTANCE - GOAL FOR LAB MEETING
     df_metadata.loc[
         (df_metadata['Video'] == video_name) & (df_metadata['Track'] == track), 'Travelled distance (cm)'] = (np.sum(  #sum of displacements
         label_vel_tracks[track])) * rowtrack["Pixelsize"].values[0]   #covert pixels to cm
     # 3.3. AVERAGE VELOCITY
     df_metadata.loc[(df_metadata['Video'] == video_name) & (df_metadata['Track'] == track), 'Avg Velocity (cm/s)'] = (np.mean(   #mean of velocity
         label_vel_tracks[track]))*rowtrack["Pixelsize"].values[0]*rowtrack["FPS"].values[0] #covert pixels/fr to cm/s

#4. EXPORT EXCEL

with pd.ExcelWriter(resultsfolder+'Results.xlsx') as writer:
  df_metadata.to_excel(writer, sheet_name= selected_label, index=False)

##brainstorm of measures of interest
    #3.3.COVARIANCE OF VELOCITY BETWEEN TWO ANIMALS
  #win = 300
  #cov_vel = corr_roll(label_vel_track0, label_vel_track1,win) #FIXME

#4.2. TIME IN CLOSED PROXIMITY

#4.3. TIME LABEL A IN TRACK-0 WAS CLOSED TO LABEL B IN TRACK-1
