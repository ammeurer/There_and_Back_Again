#!/usr/local/bin/python

# import csv, os, fiona, json, sys, argparse
# from scipy import stats
# from rasterio import features, Affine
# from shapely.geometry import Polygon, MultiPolygon, mapping
# from fiona.crs import from_epsg
import numpy as np

# parser = argparse.ArgumentParser(description='Create Density Surface from GeoJSON points.')

# parser.add_argument('infile',
#                     help='Input GeoJSON')

# parser.add_argument('outfile',
#                     help='Output Shapefile')

# parser.add_argument('cellSize',
#                     help='Grid size of analysis raster, in meters')

# parser.add_argument('kernel',
#                     help='Kernel bandwidth')

# parser.add_argument('classes',
#                     help='Number of output classes')

# parser.add_argument('--w',
#                      help='Classification weighting')

# args = parser.parse_args()

# cellSize = int(args.cellsize)

# kernBW = float(args.kernel)

# classNumber = int(args.classes)

# if args.w == None:
#     classWeight = 0.5
# else:
#     classWeight = float(args.w)

seed_file_name = "crime_ll"
# grid_cell_size = 90

# def lnglatToXY(ll):
#     from math import pi, log, tan
#     D2R = pi / 180.0
#     A = 6378137.0
#     x = (A * float(ll[0]) * D2R)
#     print 'x', x
#     y = (A * log(tan((pi*0.25) + (0.5 * float(ll[1]) * D2R))))
#     print 'y', y
#     return x,y

# def classify(zArr,classes,weighting=0.5):
#     'convert crime kernel surface into classed surface for polygonization'
#     outRas = np.zeros(zArr.shape)
#     zMax = zArr.max()
#     zMin = zArr.min()
#     zRange = zMax-zMin
#     zInterval = zRange/float(classes)
#     print "Classifying into "+str(classes)+" classes between "+str(zMin)+" and "+str(zMax)
#     for i in range(0,classes):
#         eQint = i*zInterval+zMin
#         quant = np.percentile(zArr, i/float(classes)*100)
#         cClass = weighting*eQint+(1.0-weighting)*quant
#         outRas[np.where(zArr>cClass)] = cClass
#     return ((outRas/zMax)*256).astype(np.uint8)



# with open(args.infile, 'r') as pointFile:
#     geojson = json.loads(pointFile.read())

# Initialize list that will hold all the longitudes and latitudes
lonlat_list = []
# Open and parse lat and lon tuples from seed file
with open(seed_file_name, 'r') as seed_fh:
	for line in seed_fh:
		lat, lon = line.split()
		lonlat_list.append((float(lat), float(lon)))
	print lonlat_list	
seed_fh.close()	
# xys = []

# for ll_tup in lonlat_list:
# 	ll = lnglatToXY(ll_tup)
# 	print "ll to XY conversion result:", ll
# 	xys.append(ll)
# del lonlat_list
# print "XYS", xys
# xys = np.array(lonlat_list)
# print "XYS after np.array funct", xys

# xmin = xys[:,0].min()
# print "xmin", xmin
# xmax = xys[:,0].max()
# print 'xmax', xmax
# ymin = xys[:,1].min()
# print 'ymin', ymin
# ymax = xys[:,1].max()
# print 'ymax', ymax
# my_mgrid = np.mgrid[xmin:xmax:grid_cell_size, ymin:ymax:grid_cell_size]
# print "mygrid", my_mgrid
# print 'X', X
# print 'Y', Y
# positions = np.vstack([X.ravel(), Y.ravel()])
# print 'positions', positions
# values = np.vstack([xys[:,0], xys[:,1]])
# print 'values', values
# del xys


# print "Running gaussian kernel.."
# kernel = stats.gaussian_kde(values,bw_method=kernBW)
# Z = np.reshape(kernel(positions).T, X.shape)
# del kernel, positions, X, Y
# Ztemp = (Z*10e+10).astype(np.uint16)
# del Z

# print "Classifying..."
# Z16 = classify(Ztemp,classNumber,classWeight)
# del Ztemp
# pixel_size_x = (xmax - xmin)/Z16.shape[0]
# pixel_size_y = (ymax - ymin)/Z16.shape[1]
# upper_left_x = xmin - pixel_size_x/2.0
# upper_left_y = ymax + pixel_size_y/2.0

# transform = Affine(
#                 pixel_size_x, 0.0, upper_left_x,
#                 0.0, -pixel_size_y, upper_left_y)

# schema = { 'geometry': 'MultiPolygon', 'properties': { 'value': 'int' } }

# print "Writing to shp..."

# with fiona.collection(args.outfile, "w", "ESRI Shapefile", schema, crs=from_epsg(3857)) as outshp:
#     for feature, shapes in features.shapes(np.asarray(np.rot90(Z16.astype(np.uint8)),order='C'),transform=transform):
#         featurelist = []
#         for f in feature['coordinates']:
#             featurelist.append(Polygon(f))
#         poly = MultiPolygon(featurelist)
#         outshp.write({'geometry': mapping(poly),'properties': {'value': shapes}})







# compare function for sorting lat/lon tuples
def compare_lat_lon(a, b):
	if a[0] > b[0]:
		return 1
	elif a[0] < b[0]:
		return -1
	elif a[0] == b[0]:
		if a[1] > b[1]:
			return 1
		elif a[1] < b[1]:
			return -1
		else: 
			return 0

def compare_lat_lon_for_grid(a, b):
	# print a, b
	if a[1] > b[1]:
		return 1
	elif a[1] < b[1]:
		return -1
	elif a[1] == b[1]:
		# print "got to equals"
		if b[0] > a[0]:
			# print "got to b > a"
			return 1
		elif b[0] < a[0]:
			# print "got to b < a"
			return -1
		else: 
			# print "got to returning 0"
			return 0

def create_crime_density_grid(ll_list):

	xys = []
	granularity = 1000

	xys = np.array(ll_list)
	print "XYS after np.array funct", xys

	xmin = round(xys[:,0].min(), 3)
	print "xmin", xmin
	xmax = round(xys[:,0].max(), 3)
	print 'xmax', xmax
	ymin = round(xys[:,1].min(), 3)
	print 'ymin', ymin
	ymax = round(xys[:,1].max(), 3)
	print 'ymax', ymax
	# my_mgrid = np.mgrid[xmin:xmax:grid_cell_size, ymin:ymax:grid_cell_size]
	# print "mygrid", my_mgrid
	# sf_nw_corner = (37.8010, -122.5225)
	# sf_se_corner = (37.7079, -122.3562)
	#Create a dictionary of crime counts for each lat/lon range
	#key is tuple of lat/lon
	#value is count
	crime_counts = {}
	for lat in xrange(int(xmin*granularity), int(xmax*granularity), 1):
		for lon in xrange(int(ymax*granularity), int(ymin*granularity), -1):
			crime_counts[(lat/1000.0,lon/1000.0)] = 0

	# print crime_counts
	# print len(crime_counts.keys())
	sorted_keys = crime_counts.keys()
	sorted_keys.sort(compare_lat_lon)
	# for i in sorted_keys:
	# 	print i

	for ll in ll_list:
		# lat, lon = line.split(',')
		# lat = float(lat.replace('"', ''))
		# lon = float(lon.replace('"', '').lstrip())
		lat, lon = ll
		# print lat, lon 
		for coord in sorted_keys:
			if (lat <= coord[0]) and (lon <= coord[1]):
					crime_counts[(coord[0], coord[1])] = crime_counts.get((coord[0], coord[1]), 0) + 1
					# print "found a match for " + str(lat) + ", "  + str(lon) + " at " + str(coord[0]) + " " + str(coord[1]) + " count is "  + str(crime_counts[(coord[0], coord[1])])
					break

	return crime_counts

def format_ascii_grid(crime_density_dict):
	sorted_keys = crime_density_dict.keys()
	sorted_keys.sort(compare_lat_lon_for_grid)
	ascii_density_grid_fh = open("ascii_density_grid.asc", 'w')
	ascii_ll_grid_fh = open("ascii_ll_grid.asc", 'w')
	count_col = 0

	prev_coord_lat = sorted_keys[0][1]
	for coord in sorted_keys:
		if coord[1] != prev_coord_lat:
			ascii_density_grid_fh.write('\n')
			ascii_ll_grid_fh.write('\n')
			prev_coord_lat = coord[1]
			print count_col
			count_col = 0

		ascii_density_grid_fh.write(str(crime_density_dict[coord]))
		ascii_ll_grid_fh.write(str(coord))
		ascii_density_grid_fh.write(' ')
		ascii_ll_grid_fh.write(' ')
		count_col += 1

crime_dict = create_crime_density_grid(lonlat_list)


# test_dict = {
# 	(37.723, -123.89): 1,
# 	(37.890, -121.43): 1,
# 	(34.907, -123.589): 2,
# 	(37.723, -120.3): 1
# }
format_ascii_grid(crime_dict)

# parse_crimes()

