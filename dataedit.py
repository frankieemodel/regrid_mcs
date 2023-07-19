import numpy as np

# mask data - convert missing vals to 0s and all others to 1s
def ctnmask(masked_data):
    """
    masked_data: must be a masked np array
    """
    ctn = masked_data.squeeze()
    m = np.ma.getmask(ctn).squeeze()
    ctn_copy = np.ma.getdata(ctn).squeeze()
    ctn_copy = np.where(ctn_copy==~m,0,1)
    
    return ctn_copy

def latcut(lat_array, cleaned_data):
    """
    lat_array: 2d np lat array from MCS data
    cleaned_data: CTN data, a 2d np array cleaned using clean_ctn
    returns 2 arrays: 1d np lat array cut to bounds of cygnss lat array &
    2d np data array with lat dim cut to bounds of cygnss data
    """
    lats = lat_array[:,0]
    index_latmax = np.where(lats==39.95)[0].squeeze()
    index_latmin = np.where(lats==-39.95)[0].squeeze()
    # make sure that subset of lats using these indices is the size we want
    # needs to be 800 element array
    lat_new = lats[index_latmin:index_latmax+1]

    # use indices to cut ctn array
    ctn_copy = cleaned_data[index_latmin:index_latmax+1,:]

    return lat_new, ctn_copy

def lonarrange(lon_array, cleaned_data):
    """
    lon_array: 2d np lon array from MCS data
    cleaned_data: CTN data, a 2d np array cleaned and with bounds set by cut_lat
    returns 2 arrays: 1d np lon array rearranged to mirror cygnss lon array &
    2d np data array with lon dim rearranged in same way
    """
    ctn2 = np.copy(cleaned_data)
    lons = lon_array[0,:]

    ctn2[:,0:1800] = cleaned_data[:,1800:]
    ctn2[:,1800:] = cleaned_data[:,0:1800]

    # reorder copy of lon array
    lon_new = np.copy(lons)
    lon_new[0:1800] = lons[1800:]
    lon_new[1800:] = lons[0:1800]+360

    return lon_new, ctn2

# nearest neighbor averaging
def nnaverage(new_lat,new_lon,new_ctn):
    """
    nearest neighbor averaging for cleaned and rearranged ctn data. then subsamples lon, lat, and data to match dimensions of cygness data
    takes 3 args: 
        new_lat: rearranged 1d np lat array,
        new_lon: selected 1d lon array
        new_ctn: edited 2d ctn array
    returns 3 arrays: 
        subsampled lat_sel
        subsampled lon_sel,
        avgd and subsampled ctn_fin
    """

    # average longitude first
    # for one array add last column to beginning and chop last row off end
    ctn_w = np.empty_like(new_ctn)
    ctn_w[:,0] = new_ctn[:,-1]
    ctn_w[:,1:] = new_ctn[:,0:-1]
    ctn_e = np.copy(new_ctn)
    lon_avg = (ctn_w + ctn_e)/2

    # nearest neighbor averaging for lat
    # add a nan row to start of one array and chop end off
    ctn_n= np.empty_like(lon_avg)
    ctn_n[0,:] = np.nan
    ctn_n[1:,:] = lon_avg[0:-1,:]
    ctn_s = np.copy(lon_avg)
    ctn_avg = (ctn_n + ctn_s)/2

    # subsample data and chop off last row and column
    # starting on row 1 gets rid of 1st nan row and keeps last row
    ctn_fin = ctn_avg[1::2,0::2]

    # subsample lat/lon to match
    lat_sel = new_lat[1::2]
    lon_sel = new_lon[0::2]

    return lat_sel, lon_sel, ctn_fin