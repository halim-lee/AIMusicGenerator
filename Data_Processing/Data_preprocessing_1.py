#!/usr/bin/env python
# coding: utf-8

# In[17]:


import os
#os.chdir('D:\engsci\year 3\CLASS\APS360\Project') #Sets current working directory! #Set working directory!


# # This file contains the required code to compile all the files from the dataset, convert them into arrays and save this new dataset.

# In[10]:


# import MIDI_backconversion #Would be cleaner. Oh well.
# import MIDI_conversion2

import mido
from mido import MidiFile, Message, MidiTrack
import torch
import torchvision
import os
import numpy as np
import time
import midi
import glob  
from tqdm import tqdm
import numpy as np


# # Defining required functions

# In[11]:


def Numpy2Midi(array):                      # Defining it iteratively...
    #Start with initializing a new Mido Track:
    mid = MidiFile()
    track = MidiTrack()
    already_added = []
    for i,note in enumerate(array):         # Get the index and the note. Array must be int array             
        #print(note)
        sustain = note[3]                   # Get how long the note is on for.
        #print(sustain)
        j = 1
        track.append(Message('note_on',note = array[i,0], velocity = array[i,1],time = array[i,2])) # Add the note to the track.
        while (i+j <= array.shape[0]-1) and (sustain > array[i+j,2]):       
            # ^^ If sustain is longer than the time to the next note or we reached the last note...
            if (i+j) not in already_added:
#                 print('not already added')
                track.append(Message('note_on',note = array[i+j,0], velocity = array[i+j,1],time = array[i+j,2]))
                already_added.append([i+j])
#                 print('updated already_apped list')
            sustain = sustain - array[i+j,2] # Subtract the time to the next note.
            j += 1 #update index to check agains.
        track.append(Message('note_on',note = array[i,0], velocity = 0,time = sustain)) # Add the off note.
    mid.tracks.append(track)
    return mid

def Midi2Numpy(mid):                                #converts to numpy array removing non-note messages
    track = mid.tracks[1]                           #0th track only contains meta-messages, all notes on 1st track
    notes = np.empty([0,4])                         #4 because we're tracking: note, velocity,time and sustain.
    time = 0
    for msg in track:
        if msg.type == "note_on":                   # only count "note" messages - other inputs i.e. foot pedals are ignored
            #if msg[1] > 0: ?
            notes = np.append(notes,np.array([[msg.note, msg.velocity, msg.time + time, 0]]),axis=0)         # (note, velocity, time, sustain)
            time = 0
        else:
            time += msg.time                        #adjust time when removing other messages (time is length of note? start time of notes from start of song?)
    return notes


def NumpyGetSustain(notes):                       # Removes the zeroes
    for i, msg in enumerate(notes):
        if msg[1] > 0:                            # if velocity is not 0 (if note is being turned on)
            j = 1
            sustain = 0
            while msg[0] != notes[i+j][0]:        # while note values are different
                sustain += notes[i+j][2]          # Update sustain of ith note with i+jth note's time.
                j += 1                            #search for next message with same note i.e. message telling that note was released
            notes[i,3] = sustain + notes[i+j][2]  # once next appearance of note identified, updat ith note's sustain as time on until next note.
    time = 0
    for i, msg in enumerate(notes):               
        if msg[1] > 0:                            # If velocity is not 0
            notes[i,2] += time                    # Update the ith note's time
            time = 0
        else:
            time += msg[2]                        #adjust time
    notes = notes[notes[:,1] > 0]                 #filter for notes with positive velocities (note presses)
    return notes


def CountTracks(directory):          #Count files and tracks in folder
    trackCount = 0
    fileCount = 0
    for file in os.listdir(directory):
        if file.endswith(".midi"):
            fileCount += 1
            midiDir = MidiFile(directory+"/"+file)
            for track in midiDir.tracks: # Locates the tracks in a 'song.midi'
                trackCount += 1 # Counts tracks.
    print(fileCount+" files")
    print(trackCount+" tracks")

    
def PrintMessages(mid):                # print midi messages
    for i, track in enumerate(mid.tracks): # Iterates through tracks and also outputs the index.
        print('Track {}: {}'.format(i, track.name))
        for msg in track:
            print(msg)

            
def PrintSomeMessages(mid):             #print first 200 midi messages
    track = mid.tracks[1]
    for i,msg in enumerate(track):
        if i < 200:
            print(msg)
            
def cleanupMessages(mid):
    track = mid.tracks[1]
    track2 = []
    for msg in track:
        if msg.type == "note_on":
            track2.append(msg)
    mid.tracks[1] = track2
            


# In[12]:


#Note: The dataset needs to be in the same directory. Set working directory above.
# Process: 
# 1) Import the dataset (likely requires a dataloader so it can be done in batches)
# - Will require unzipping it into the machine
# - Will then require loading it into a variable.
# 2) For each entry of the dataset, call MIDI2Numpy on the datasample.
# 3) Save the outputs (Again, likely need to do this in batches if dataset too large)


# In[13]:


#Only if required (using colab)
# !unzip '\datasets\maestro-v2.0.0-midi' -d '/root/datasets' #Customize data directory to your machine.


# In[19]:


#Will use DatasetFolder: https://pytorch.org/docs/stable/torchvision/datasets.html#imagefolder (scroll up or ctrl F)

unprocessed_midis = torchvision.datasets.DatasetFolder('D:/engsci/year 3/CLASS/APS360/Project/datasets/maestro-v2.0.0-midi/maestro-v2.0.0','any')


# In[ ]:




