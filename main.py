'''
This is the main code to run analysis on data extracted from SLEAP.
If you are using this project, I recommend setting it in the same environment as SLEAP so
you don´t have to re-download the packages that are required for analysis.
Some scripts were used from the website sleap.ai: https://sleap.ai/notebooks/Analysis_examples.html
'''
import h5py
from functions import fill_missing, select_label, smooth_diff, corr_roll
from visualizations import plot_tracks, plot_velocity, plot_velocity2d


#1. UPLOAD DATA #for now I am using one file then it will be a loop

filedirectory = '/mnt/datafast/vanesa/SLEAP_projects/analysis/'
file = 'Habdishab2rats.slp.250324_104922.predictions.000_2021_03_05_habdishab_exp_sgxE8_rat1166_e1.analysis.h5'
filename = filedirectory + file

with h5py.File(filename, "r") as f:
    dset_names = list(f.keys())
    locations = f["tracks"][:].T
    node_names = [n.decode() for n in f["node_names"][:]]
    video_name = file[-22:-12]

#readout of characteristics - I will make it a function
print("===filename===")
print(filename)
print()

frame_count, node_count, _, instance_count = locations.shape

print("frame count:", frame_count)
print("node count:", node_count)
print("instance count:", instance_count)

#2. FILL MISSING VALUES
locations = fill_missing(locations)

#3. VISUALISATIONS
#3.1.A LABEL OF CHOICE ACROSS VIDEO FOR BOTH ANIMALS
selected_index, selected_label = select_label(node_names) #define labels index and location
label_loc = locations[:, selected_index, :, :] #extract locations of the selected label
plot_tracks(video_name,label_loc, selected_label) #plot the tracks of both animals for the same selected label

#3.2. VELOCITY FOR ONE ANIMAL (track is an animal)
track = 0 #choose the animal- It can be track 0 or track 1. #FIXME change to dialog in the future
track_name = 'track'+ str(track)
label_vel_track = smooth_diff(label_loc[:, :, track])
plot_velocity(label_loc,label_vel_track, video_name, selected_label, track_name)
plot_velocity2d(label_loc,label_vel_track, video_name, selected_label,track_name)

#3.3.COVARIANCE OF VELOCITY BETWEEN TWO ANIMALS
win = 300
label_vel_track0 = smooth_diff(label_loc[:, :, 0])
label_vel_track1 = smooth_diff(label_loc[:, :, 1])
cov_vel = corr_roll(label_vel_track0, label_vel_track1,win) #FIXME

#4.CALCULATE MEASUREMENTS OF INTEREST
#4.1. TRAVELLED DISTANCE - GOAL FOR LAB MEETING

#I am going to calculate for track 0 then track 1. Maybe I do a loop later when I am refining the code we'll see.


#4.2. TIME IN CLOSED PROXIMITY

#4.3. TIME LABEL A IN TRACK-0 WAS CLOSED TO LABEL B IN TRACK-1