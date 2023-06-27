from osgeo import gdal
import numpy as np
import rasterio
from osgeo import gdal
import numpy as np
import matplotlib.pyplot as plt


# DEM 文件路径
demPath = r'D:\LPJGUESS\Data for input\1Krycklan Catchment\DEM\Krycklan_2015_DEM_0.5m\Krycklan_2015_DEM_50m.tif'
slopefile = r'D:\LPJGUESS\Data for input\1Krycklan Catchment\DEM\Krycklan_2015_DEM_0.5m\Krycklan_2015_SLOPE_50m.tif'
aspectfile = r'D:\LPJGUESS\Data for input\1Krycklan Catchment\DEM\Krycklan_2015_DEM_0.5m\Krycklan_2015_ASPECT_50m.tif'



with rasterio.open(demPath) as dataset:
    dem=dataset.read(1)
    plt.imshow(dem, cmap="magma", vmin=100, vmax=400)
    plt.colorbar(label='DEM(m)')
    plt.savefig('Krycklan_2015_DEM_50m.png',  bbox_inches= 'tight',dpi=300)
    plt.show()

gdal.DEMProcessing(slopefile, demPath, 'slope', options = '-p')
with rasterio.open(slopefile) as dataset:
    slope=dataset.read(1)
    print('slope:',slope)
    plt.imshow(slope, cmap="magma", vmin=0, vmax=90)
    plt.colorbar(label='Slope(degree)')
    plt.savefig('Krycklan_2015_SLOPE_50m.png', bbox_inches='tight', dpi=300)
    plt.show()

gdal.DEMProcessing(aspectfile, demPath, 'aspect')
with rasterio.open(aspectfile) as dataset:
    aspect=dataset.read(1)
    print('aspect:',aspect)
    plt.imshow(aspect, cmap="magma", vmin=0, vmax=360)
    plt.colorbar(label='Aspect(degree)')
    plt.savefig('Krycklan_2015_ASPECT_50m.png', bbox_inches='tight', dpi=300)
    plt.show()





