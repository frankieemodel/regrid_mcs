# regrid_mcs
designed to run on data for *one* time step ie 2d data... so the function extracts date and time for 1 timestep in ncwtools.getdate(filename) and creates a netcdf file with 1D time!

## Main script is ctngrid_loop.py
### variables to change
14: path_to_data= '/Path/to/data/' path to dir containing files you want processed
15: svdir='/Path/to/new/data/' path to dir where you want to save new data
### to_test
19: uncomment/comment this line depending on whether or not you're testing, lest you be waiting a loooong time for your test to run

each loop outputs the filename of the new file to show that the loop is completing - could disable this if you don't want to output 8k filenames - just comment out line 63

loop will run and tell you how long it took in seconds


## time note - in ncwtools.makefile
line 42: changed size of 'time' when creating dimension, from unlimited to 1 because it *significantly* decreased size and processing time (by oom) 
  - this would need to be changed if working with 3d data
  - maybe change this to a varible that changes with size of time var
  - but currently the time 'variable' is just one datetime object, so leaving it for now

