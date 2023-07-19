import datetime as dt
import os
import netCDF4 as nc

def getdate(filename):
    """
    from full filepath date of data collection is extracted. returns date as a datetime object
    """
    test_fn = filename.split('/')[-1]
    year,month,day = test_fn[9:13],test_fn[13:15],test_fn[13:15]
    time = test_fn[18:22]
    date = '{y}{m}{d}-{t}'.format(y=year,m=month,d=day,t=time)
    # make dt object
    dt_date = dt.datetime.strptime(date, '%Y%m%d-%H%M')
    
    return dt_date

# NC FILE
def makefile(src_path, sv_dir, lat_sel, lon_sel, ctn_fin):
    """
    5 required inputs: 
    src_path - complete original filepath from MCS data (for date)
    !sv_dir - folder to save new data !V IMPORTANT ** IF running in loop could save A TON OF DATA in wrong location if not careful
    lat_sel - 1d lat array
    lon_sel - 1d lat array
    ctn_fin - CTN data 2d np array to be written to file
    returns nothing but creates 
    """
    # get filename using date from og file
    dt_date = getdate(src_path)
    # format date and format filename
    sv_date = dt_date.strftime("%Y%m%d-%H%M")
    sv_fn = 'mcs_ctn_{date}.nc'.format(date=sv_date)
    # specify path to save new file
    # svdir = '/Volumes/T7/Data/mcs/'
    svpath = os.path.join(sv_dir,sv_fn)

    # open nc file to write
    ds = nc.Dataset(svpath, 'w', format='NETCDF4')

    # create 3 dimensions
    time = ds.createDimension('time', None)
    lat = ds.createDimension('lat', lat_sel.shape[0])
    lon = ds.createDimension('lon', lon_sel.shape[0])
    
    # create variables and their properties
    # Create time
    calendar = 'standard'
    time_units = 'hours since 1970-01-01 00:00'
    # Write timestamps to netCDF file using 64bit integer
    time = ds.createVariable('time', 'i4', ('time'))
    time[:] = nc.date2num(dt_date, units=time_units, calendar=calendar)

    #create lat/lon
    # longitude
    lon = ds.createVariable('lon', 'f4', ('lon'))
    lon.standard_name = "longitude"
    lon.units = "degrees_east"
    lon.axis = 'X'
    # latitude
    lat = ds.createVariable('lat', 'f4', ('lat'))
    lat.standard_name = "latitude"
    lat.units = "degrees_north"
    lat.axis = 'Y'

    # fill lat/lon with their rearranged and sampled values
    lat[:] = lat_sel
    lon[:] = lon_sel

    # creating var in question:

    # print(data_file[var_name].standard_name + " std name from file")
    ctn = ds.createVariable('cloudtracknumber', 'i4', ('time', 'lat', 'lon'))
    ctn.units = 'unitless'
    ctn.long_name = "MCS cloud track number"

    # fill ctn with values
    ctn[:] = ctn_fin

    # Add global attributes
    ds.title = "MCS data, Cloud Track Number: Regridded"
    ds.data_collected = dt_date.strftime('%m/%d/%Y %H:%M')
    today = dt.datetime.today()
    ds.Created_on = "Created by Frankie Modell " + today.strftime("%m/%d/%y")

    # file must be closed
    ds.close()

    return sv_fn