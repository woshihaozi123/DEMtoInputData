# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np

import matplotlib.pyplot as plt
import math
from DEMAspecttoData import removemissingvalue

from DEMbinplot import Elevationgroupbarplot,EqualwidthbarPlot
from DEMAspecttoData import read_tif,writetotxt
from ClassifyMethod import EqualnumberClassify,EqualwidthClassify

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('start----------------------------------------')
    demPath = r'D:\LPJGUESS\Data for input\1Krycklan Catchment\DEM\Krycklan_2015_DEM_0.5m\Krycklan_2015_DEM_50m.tif'
    banddata=read_tif(demPath)
    data=removemissingvalue(banddata,missingvalue=0).flatten()
    print('Total number of gridcell:',len(data))
    sorted_data = np.sort(data)
    categories = ['elevation1', 'elevation2', 'elevation3', 'elevation4']
    num_bins=4

    #classify and draw
    print('classify and draw-----------------------------')

    hist1, meanvalues1, groupvalues1,bins1 = EqualwidthClassify(sorted_data,num_bins)
    print('Elevation fractions:',hist1/sum(hist1))
    print('Elevation meanvalue:', meanvalues1)
    Elevationgroupbarplot(categories,hist1/sum(hist1),[round(x, 2) for x in meanvalues1],[round(x, 2) for x in bins1],'DEM classified by equal width')

    hist2, meanvalues2, groupvalues2,bins2=EqualnumberClassify(sorted_data, num_bins)
    print('Elevation fractions:',hist2/sum(hist2))
    print('Elevation meanvalue:', meanvalues2)
    Elevationgroupbarplot(categories,hist2/sum(hist2),[round(x, 2) for x in meanvalues2],[round(x, 0) for x in bins2],'DEM classified by equal number')

    EqualwidthbarPlot(data, [int(round(x, 0)) for x in bins1],1,[round(x, 0) for x in hist1/sum(hist1)],[round(x, 2) for x in meanvalues1],'DEM bin classified by equal width')
    EqualwidthbarPlot(data, [int(round(x, 0)) for x in bins2],1,[round(x, 0) for x in hist2/sum(hist2)],[round(x, 2) for x in meanvalues2],'DEM bin classified by equal number')

