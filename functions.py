'''
In this script all the functions for data analysis that are called in main.py are stored.
'''


from scipy.interpolate import interp1d
import numpy as np
import tkinter as tk
from tkinter import ttk
from scipy.signal import savgol_filter
import pandas as pd
import os
import h5py

def fill_missing(Y, kind="linear"):
    """Fills missing values independently along each dimension after the first."""

    # Store initial shape.
    initial_shape = Y.shape

    # Flatten after first dim.
    Y = Y.reshape((initial_shape[0], -1))

    # Interpolate along each slice.
    for i in range(Y.shape[-1]):
        y = Y[:, i]

        # Build interpolant.
        x = np.flatnonzero(~np.isnan(y))
        f = interp1d(x, y[x], kind=kind, fill_value=np.nan, bounds_error=False)

        # Fill missing
        xq = np.flatnonzero(np.isnan(y))
        y[xq] = f(xq)

        # Fill leading or trailing NaNs with the nearest non-NaN values
        mask = np.isnan(y)
        y[mask] = np.interp(np.flatnonzero(mask), np.flatnonzero(~mask), y[~mask])

        # Save slice
        Y[:, i] = y

    # Restore to initial shape.
    Y = Y.reshape(initial_shape)

    return Y

def select_label(node_names):
    # Store selections in a mutable object (like a dictionary)
    selection = {"index": None, "label": None}

    def on_select(event):
        # Update the selection dictionary
        selection["index"] = listbox.curselection()[0]
        selection["label"] = listbox.get(selection["index"])
        root.destroy()  # Close the window

    root = tk.Tk()
    root.title("Select a Node")

    label = ttk.Label(root, text="Select a node from the list:")
    label.pack(pady=10)

    listbox = tk.Listbox(root, height=5, selectmode=tk.SINGLE)
    listbox.pack(pady=10, padx=20)

    for name in node_names:
        listbox.insert(tk.END, name)

    listbox.bind('<<ListboxSelect>>', on_select)
    root.mainloop()  # Blocks until window is destroyed

    # After the window closes, return the selection
    return selection["index"], selection["label"]

def smooth_diff(node_loc, win=25, poly=3):
    """
    node_loc is a [frames, 2] array

    win defines the window to smooth over

    poly defines the order of the polynomial
    to fit with

    """
    node_loc_vel = np.zeros_like(node_loc)

    for c in range(node_loc.shape[-1]):
        node_loc_vel[:, c] = savgol_filter(node_loc[:, c], win, poly, deriv=1)

    node_vel = np.linalg.norm(node_loc_vel, axis=1)

    return node_vel

def corr_roll(datax, datay, win): #FIXME
    s1 = pd.Series(datax)
    s2 = pd.Series(datay)

    return np.array(s2.rolling(win).corr(s1))

def reading_h5files(file,filepath):
    filename = os.path.join(filepath, file)
    with h5py.File(filename, "r") as f:
        dset_names = list(f.keys())
        locations = f["tracks"][:].T
        node_names = [n.decode() for n in f["node_names"][:]]
        video_name = file[-22:-12]

        return filename, dset_names, locations, node_names, video_name
