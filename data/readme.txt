

MIDI_files_original			contains all original MIDI files from Maestro

numpy_files				contains midi files as .csv files - easy to read but kinda memory inefficient

MIDI_files_processed			contains midi files reconverted from numpy
					this is what a theoretical output might look like since it doesnt have program msgs

numpy_onehot				same as numpy_files but encoded as one-hot for notes
					format is:
					[C, C#, D, D#, E, F, F#, G, G#, A, A#, B, octave, velocity, time, sustain]			

Notes_Dataset				NEEDS TO BE DOWNLOADED - file too big:
					https://drive.google.com/file/d/1mTXywGuZjaXWVXF8ZM_0Td4aIzZ1e2op/view?usp=sharing
					Contains tensors for 20-note samples