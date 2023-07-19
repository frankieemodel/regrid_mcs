import numpy as np
import netCDF4 as nc
import os
# import datetime as dt
import dataedit
import ncwtools
import time

# get the start time
st = time.time()

# file specification must be done in main boss file
path_to_data = '/Volumes/T7/MCS_PNNL/'
svdir = '/Volumes/T7/Data/mcs/'
# get list of file names
file_list = os.listdir(path_to_data)
# name of variable to get from the data file
var = 'cloudtracknumber'

# loop over file names
for fn in file_list[:5]:
    # join file dir and file name
    data_file = os.path.join(path_to_data,fn)
    # could import data and mask in one fxn but need opened file later also, so would be redundant
    dataset = nc.Dataset(data_file)
    ctn=dataset[var][:]
    mcs_lat = np.ma.getdata(dataset['latitude'][:])
    mcs_lon = np.ma.getdata(dataset['longitude'][:])

    # clean up masked data ie convert missing vals '--' to zeros 
    # and all others to ones
    masked_ctn = dataedit.ctnmask(ctn)

    # edit the lat array and the lat dimension of ctn 
    # so that bounds are same as cygnss data ~[-39.9:39.9]
    new_lat, lat_ctn = dataedit.latcut(mcs_lat, masked_ctn)

    # edit the lon array and lon dimension of ctn 
    # convert from [-180:180] to [0:360]
    new_lon, new_ctn = dataedit.lonarrange(mcs_lon, lat_ctn)
    # print(new_lon.shape)
    # use nearest neighbor averaging on ctn data and then 
    # subsample data and lat/lon arrays to halve size of dims
    lat_sel, lon_sel, ctn_fin = dataedit.nnaverage(new_lat, new_lon, new_ctn)

    # print(lon_sel.shape)
    # Save data to new nc file
    # get date of data collection from filename
    dt_date = ncwtools.getdate(data_file)

    # create netcdf file

    new_fn = ncwtools.makefile(
                        data_file, 
                        svdir, 
                        lat_sel, 
                        lon_sel, 
                        ctn_fin)
    print(new_fn)

    # nothing returned but file should save...
    # get the end time
et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
    