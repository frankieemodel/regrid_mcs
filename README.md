# regrid_mcs
designed to run a loop on a folder of mcs data files each containing *one* time step ie 2d data... 
- so it takes MCS datafiles at single timesteps
- gets data for 1 variable, 'Cloud Track Number,'
- regrids it to match cygnss data lat/lon dimensions,
- extracts date and time from original filenames for each timestep
- and creates a new netcdf file containing the regridded data for each single timestep

## Main script is ctngrid_loop.py
### variables to change
13: path_to_data= '/Path/to/data/' path to dir containing files you want processed
15: svdir='/Path/to/new/data/' path to dir where you want to save new data
### to test
20: uncomment/comment this line depending on whether or not you're testing, lest you be waiting a loooong time for your test to run

### outputs
each loop outputs the filename of the new file to show that the loop is completing - could disable this if you don't want to output 8k filenames - just comment out line 62

loop will run and tell you how long it took in seconds


## time note - in ncwtools.makefile
line 42: changed size of 'time' when creating dimension, from unlimited to 1 because it *significantly* decreased size and processing time (by oom) 
  - this would need to be changed if working with 3d data
  - maybe change this to a varible that changes with size of time var
  - but currently the time 'variable' is just one datetime object, so leaving it for now

