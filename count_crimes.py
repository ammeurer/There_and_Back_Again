#!/usr/local/bin/python

import numpy as np



seed_file_name = "crime_ll"


# Initialize list that will hold all the longitudes and latitudes
lonlat_list = []
# Open and parse lat and lon tuples from seed file
with open(seed_file_name, 'r') as seed_fh:
	for line in seed_fh:
		lat, lon = line.split()
		lonlat_list.append((float(lat), float(lon)))
	print lonlat_list	
seed_fh.close()	


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


