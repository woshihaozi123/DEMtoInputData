from osgeo import gdal
import numpy as np
import rasterio
from ClassifyMethod import EqualnumberClassify,EqualwidthClassify
import os
def removemissingvalue(array,missingvalue):
    # replace missing with nan
    array[array < missingvalue] = np.nan
    non_nan_values = array[~np.isnan(array)]
    min_value = np.min(non_nan_values)
    max_value = np.max(non_nan_values)
    mean_value = np.mean(non_nan_values)
    print("Non-NaN Minimum Value:", min_value)
    print("Non-NaN Maximum Value:", max_value)
    print("Non-NaN mean value:", mean_value)
    return array #use flatten() from 2d to 1D


def read_tif(file_path):
    # Open the .tif file
    dataset = gdal.Open(file_path)

    # Check if the file was successfully opened
    if dataset is None:
        print("Failed to open the file")
        return None

    # Get basic information about the raster data
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    num_bands = dataset.RasterCount

    print("Raster Width:", width)
    print("Raster Height:", height)
    print("Number of Bands:", num_bands)

    band_data  =[]
    # Read the data for each band
    for band_num in range(1, num_bands + 1):
        band = dataset.GetRasterBand(band_num)
        band_data = band.ReadAsArray(0, 0, width, height)

        # Process the band data
        # You can perform further processing or analysis on each band's data

        # Print statistics of the band data
        print("Statistics for Band", band_num, ":")
        #print("Minimum value:", band_data.min())
        #print("Maximum value:", band_data.max())
        #print("Mean value:", band_data.mean())

    # Close the dataset
    dataset = None
    return band_data

def calculate_aspect(dem_file):
    # 打开 DEM 文件
    dataset = gdal.Open(dem_file, gdal.GA_ReadOnly)

    # 读取 DEM 数据
    dem_band = dataset.GetRasterBand(1)
    dem_array = dem_band.ReadAsArray()

    # 计算 DEM 的坡向
    aspect_array = gdal.DEMProcessing('', dataset, 'aspect')

    # 释放资源
    dataset = None
    print("aspect_array:", aspect_array)
    return aspect_array

def calculate_slope(dem_file, cell_size):
    # 打开 DEM 文件
    dataset = gdal.Open(dem_file, gdal.GA_ReadOnly)

    # 读取 DEM 数据
    dem_band = dataset.GetRasterBand(1)
    dem_array = dem_band.ReadAsArray()

    # 计算 DEM 的水平和垂直梯度
    x_gradient = np.gradient(dem_array, cell_size, axis=1)
    y_gradient = np.gradient(dem_array, cell_size, axis=0)

    # 计算 DEM 的坡度
    slope_array = np.arctan(np.sqrt(x_gradient**2 + y_gradient**2))

    # 释放资源
    dataset = None

    return slope_array


def writetotxt(lonlist,latlist,data,filestr):
    with open(filestr, 'w') as file:
        file.write(str('Lon') + '\t' + str('Lat') + '\t' + '\t'.join(['top'+str(i) for i in range(1,17)]) + '\n')

        for lon,lat,row in zip(lonlist,latlist,data):
            print("row",row.tolist())
            file.write(str(lon)+'\t'+str(lat)+'\t'+'\t'.join(map(str, row.tolist())) + '\n')

# Read data
demPath = r'D:\LPJGUESS\Data for input\1Krycklan Catchment\DEM\Krycklan_2015_DEM_0.5m\Krycklan_2015_DEM_50m.tif'
slopefile = r'D:\LPJGUESS\Data for input\1Krycklan Catchment\DEM\Krycklan_2015_DEM_0.5m\Krycklan_2015_SLOPE_50m.tif'
aspectfile = r'D:\LPJGUESS\Data for input\1Krycklan Catchment\DEM\Krycklan_2015_DEM_0.5m\Krycklan_2015_ASPECT_50m.tif'

demdataset= rasterio.open(demPath)
demdata=demdataset.read(1)
dem = np.array(removemissingvalue(demdata, missingvalue=0))
demvaluelist=dem.flatten()

slopedataset=rasterio.open(slopefile)
slopedata=slopedataset.read(1)
slope = np.array(removemissingvalue(slopedata, missingvalue=0))
slopevaluelist=slope.flatten()

aspectdataset= rasterio.open(aspectfile)
aspectdata=aspectdataset.read(1)
aspect = np.array(removemissingvalue(aspectdata, missingvalue=0))
aspectvaluelist=aspect.flatten()


num_bins = 4 #4 elevation * 4 aspect
###classify
print('Total number of DEM gridcell:', len(demvaluelist))
demsorted_data = np.sort(demvaluelist)
demcategories = ['elevation1', 'elevation2', 'elevation3', 'elevation4']

print('Total number of Aspect gridcell:', len(aspectvaluelist))
aspectsorted_data = np.sort(aspectvaluelist)
aspectcategories = ['East', 'West', 'South', 'North']

def AspectClassify(data, bins):
    # num of class
    print('Num of equal width classes:', len(bins))
    num_bins=len(bins)

    hist, _ = np.histogram(data, bins=bins)
    bins1 = bins[1:-1]
    groups = np.digitize(data, bins1)
    num_bins1 = len(bins1)

    meanvalues=[];
    groupvalues=[];
    for i in range(0,num_bins1+1):
        if(i==0):
            group_data = np.array(data)[np.logical_or(groups == num_bins1, groups == i)]
            groupmean_value = np.nanmean(group_data)
            meanvalues.append(groupmean_value)
            groupvalues.append(group_data)
        else:

            group_data = np.array(data)[groups == i]
            groupmean_value = np.nanmean(group_data)
            meanvalues.append(groupmean_value)
            groupvalues.append(group_data)


    hist[0]=hist[0]+hist[num_bins-2]
    hist= np.delete(hist, num_bins-2)

    print("Histogram:", hist)
    print("Bins:", bins1)
    print("meanvalues:", meanvalues)

    #print("groupvalues:", groupvalues)
    return hist, np.array(meanvalues),groupvalues,np.array(bins)



hist_dem, meanvalues_dem, groupvalues_dem, bins_dem = EqualwidthClassify(demsorted_data, num_bins)
print('Elevation fractions:', hist_dem / sum(hist_dem))
print('Elevation meanvalue:', meanvalues_dem)


hist_aspect, meanvalues_aspect, groupvalues_aspect, bins_aspect = AspectClassify(aspectsorted_data, [0,45,135,225,315,360])
print('aspect fractions:', hist_aspect / sum(hist_aspect))
print('aspect meanvalue:', meanvalues_aspect)

elevationnum=range(1,num_bins+1)

fraction_data=np.zeros((1, 16))
dem_data=np.zeros((1, 16))
aspect_data=np.zeros((1, 16))
slope_data=np.zeros((1, 16))

for  i in range(0,num_bins):
    aspect_elevation_i= aspect[(dem >= bins_dem[i]) & (dem <= bins_dem[i + 1])]
    aspectsorted_data_i = np.sort(aspect_elevation_i.flatten())
    hist_aspect_i, meanvalues_aspect_i, groupvalues_aspect_i, bins_aspect_i = AspectClassify(aspectsorted_data_i,[0,45, 135, 225, 315,360])

    for j in range(0, num_bins):#0,1,2,3
        fraction_data[0,i*4+j]=((hist_dem[i] / sum(hist_dem))*( hist_aspect_i[j]/sum(hist_aspect_i)))
        aspect_data[0,i*4+j]=(meanvalues_aspect_i[j])
        if(j==0):
            slope_elevationi_aspectj = slope[
                np.logical_and(np.logical_and((dem >= bins_dem[i]), (dem <= bins_dem[i + 1])),
                               np.logical_or(np.logical_and((aspect >= bins_aspect_i[i]),
                                                            (aspect <= bins_aspect_i[i + 1])),
                                             np.logical_and((aspect >= bins_aspect_i[num_bins]),
                                                            (aspect <= bins_aspect_i[num_bins + 1]))))]#merge aspect between 0-45 315-360

            meanslope_elevationi_aspectj = np.nanmean(slope_elevationi_aspectj)
            slope_data[0, i * 4 + j] = (meanslope_elevationi_aspectj)

            dem_elevationi_aspectj = dem[np.logical_and(np.logical_and((dem >= bins_dem[i]), (dem <= bins_dem[i + 1])),
                                                        np.logical_or(np.logical_and((aspect >= bins_aspect_i[i]),
                                                                                     (aspect <= bins_aspect_i[i + 1])),
                                                                      np.logical_and(
                                                                          (aspect >= bins_aspect_i[num_bins]),
                                                                          (aspect <= bins_aspect_i[num_bins + 1]))))]#merge 0-45 315-360
            meandem_elevationi_aspectj = np.nanmean(dem_elevationi_aspectj)
            dem_data[0, i * 4 + j] = (meandem_elevationi_aspectj)

        else:
            slope_elevationi_aspectj = slope[
                np.logical_and(np.logical_and((dem >= bins_dem[i]), (dem <= bins_dem[i + 1])),
                               np.logical_and((aspect >= bins_aspect_i[i]), (aspect <= bins_aspect_i[i + 1])))]
            meanslope_elevationi_aspectj = np.nanmean(slope_elevationi_aspectj)
            slope_data[0, i * 4 + j] = (meanslope_elevationi_aspectj)

            dem_elevationi_aspectj = dem[np.logical_and(np.logical_and((dem >= bins_dem[i]), (dem <= bins_dem[i + 1])),
                                                        np.logical_and((aspect >= bins_aspect_i[i]),
                                                                       (aspect <= bins_aspect_i[i + 1])))]
            meandem_elevationi_aspectj = np.nanmean(dem_elevationi_aspectj)
            dem_data[0, i * 4 + j] = (meandem_elevationi_aspectj)

    #data = [[1, 2, 3],
    #        [4, 5, 6],
    #        [7, 8, 9]]

lonlist=[19.75]
latlist=[64.25]

# Get the current directory
current_dir = os.getcwd()
writetotxt(lonlist,latlist,np.round(dem_data, decimals=4),current_dir+r'\output\file\elevation_16layers.txt')
writetotxt(lonlist, latlist, np.round(fraction_data, decimals=4), current_dir+r'.\output\file\fraction_16layers.txt')
writetotxt(lonlist, latlist, np.round(aspect_data, decimals=4), current_dir+r'.\output\file\aspect_16layers.txt')
writetotxt(lonlist, latlist, np.round(slope_data, decimals=4), current_dir+r'.\output\file\slope_16layers.txt')
