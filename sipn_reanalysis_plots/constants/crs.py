from cartopy import crs

CRS_EPSG_NUM = 3413
CRS_EPSG_STR = f'EPSG:{CRS_EPSG_NUM}'

# TODO: How to use 3413 with cartopy?
CRS = crs.NorthPolarStereo(central_longitude=-45)
# CRS = crs.epsg(CRS_EPSG_NUM)
