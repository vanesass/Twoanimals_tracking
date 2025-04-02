'''
In this script all the functions for visualizations that are called in main.py are stored.
'''

import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def plot_tracks(video_name, label_loc, selected_label, plot_path):
    """
    Plots tracking data for two tracks (0 and 1)

    Args:
        label_loc (numpy.ndarray): 3D array containing tracking data
        selected_label (str): The label/title to use for the plots
    """
    # Set up plot style
    sns.set_theme(style='ticks', context='notebook', font_scale=1.2)
    mpl.rcParams['figure.figsize'] = [15, 6]

    # First plot - time series of locations
    plt.figure()
    plt.plot(label_loc[:, 0, 0], 'y', label='track-0')
    plt.plot(label_loc[:, 0, 1], 'g', label='track-1')
    plt.plot(-1 * label_loc[:, 1, 0], 'y')
    plt.plot(-1 * label_loc[:, 1, 1], 'g')
    plt.legend(loc="center right")
    plt.title(f'{video_name,selected_label} locations')
    plt.xlabel('Time (frames)')  # X-axis label for Plot 1
    plt.ylabel('Dimension 1 | Dimension 2')  # X-axis label for Plot 1
    plot1 = plot_path + 'coordinates.png' #save figure
    plt.savefig(plot1)#save figure

    # Second plot - 2D tracks
    plt.figure(figsize=(7, 7))
    plt.plot(label_loc[:, 0, 0], label_loc[:, 1, 0], 'y', label='track-0')
    plt.plot(label_loc[:, 0, 1], label_loc[:, 1, 1], 'g', label='track-1')
    plt.legend()

    # Formatting for second plot
    plt.xlim(0, 1024)
    plt.xticks([])
    plt.ylim(0, 1024)
    plt.yticks([])
    plt.title(f'{video_name,selected_label} tracks')
    plot2 = plot_path + 'trajectories.png' #save figure
    plt.savefig(plot2) #save figure

    # Display all figures
    plt.show()

def plot_velocity(label_loc,label_vel_track, video_name, selected_label,track_name,track, plot_path):
    #First plot of velocity
    fig = plt.figure(figsize=(15, 7))
    ax1 = fig.add_subplot(211)
    ax1.plot(label_loc[:, 0, track], 'k', label='x')
    ax1.plot(-1 * label_loc[:, 1, track], 'k', label='y')
    ax1.legend()
    ax1.set_xticks([])
    ax1.set_title( f'{video_name, selected_label,track_name}')

    ax2 = fig.add_subplot(212, sharex=ax1)
    im = ax2.imshow(label_vel_track[:, np.newaxis].T, aspect='auto', vmin=0, vmax=10, cmap='cool')
    ax2.set_yticks([])
    ax2.set_title( f'{video_name, selected_label,track_name} - Velocity')
    # Add colorbar for velocity
    cbar = fig.colorbar(im, ax=ax2, orientation='vertical')
    cbar.set_label('Velocity (units)')  # Replace with your actual units
    plot3 = plot_path + track_name + 'velocityvstime.png'  # save figure
    plt.savefig(plot3)  # save figure

    # Second plot of velocity
    fig = plt.figure(figsize=(15, 6))
    ax1 = fig.add_subplot(121)
    ax1.plot(label_loc[:, 0, track], label_loc[:, 1, track], 'k')
    ax1.set_xlim(0, 1024)
    ax1.set_xticks([])
    ax1.set_ylim(0, 1024)
    ax1.set_yticks([])
    ax1.set_title(f'{video_name, selected_label,track_name} - Thorax tracks')

    kp = label_vel_track
    vmin = 0
    vmax = 10

    ax2 = fig.add_subplot(122)
    im = ax2.scatter(label_loc[:, 0, track], label_loc[:, 1, track], c=kp, s=4, vmin=vmin, vmax=vmax, cmap='cool')
    ax2.set_xlim(0, 1024)
    ax2.set_xticks([])
    ax2.set_ylim(0, 1024)
    ax2.set_yticks([])
    ax2.set_title(f"{video_name}, {selected_label}, {track_name}\n"  # First line
                "Thorax tracks colored by magnitude of fly speed")  # Second line)
    # Add colorbar for velocity
    cbar = fig.colorbar(im, ax=ax2, orientation='vertical')
    cbar.set_label('Velocity (units)')  # Replace with your actual units
    plot4 = plot_path + track_name + 'velocityontrajectory.png'  # save figure
    plt.savefig(plot4)  # save figure

    plt.show()#display all figures

def plot_covariance(label_vel_track0, label_vel_track1, cov_vel):
    fig, ax = plt.subplots(2, 1, sharex=True, figsize=(15, 6))
    ax[0].plot(label_vel_track0, 'y', label='fly-0')
    ax[0].plot(label_vel_track1, 'g', label='fly-1')
    ax[0].legend()
    ax[0].set_title('Forward Velocity')

    ax[1].plot(cov_vel, 'c', markersize=1)
    ax[1].set_ylim(-1.2, 1.2)
    ax[1].set_title('Covariance')

    fig.tight_layout()
    plt.show()
