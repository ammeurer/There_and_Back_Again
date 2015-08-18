#!/usr/local/bin/python
import re
import datetime
# Pull crime data from seed file and format in my own crime db
def add_crime_data():
	crime_fh = open('dummy.csv')
	f = open('dummy_ll', 'w')

	for row in crime_fh:
		field_list = row.split(',')
		# crime_type = field_list[1] 
		lat = field_list[-2][2:]
		lon = field_list[-1][:-3]
		# find_date = None
		# crime_date = None
		# for i in field_list:
		# 	find_date = re.match('(\d{2})/(\d{2})/(\d{4})', i)
		# 	if find_date is not None:
		# 		# print find_date.group(3), find_date.group(1), find_date.group(2)
		# 		crime_date = datetime.datetime(int(find_date.group(3)), int(find_date.group(1)), int(find_date.group(2)))

		# print "<Crime_type=%s Lat=%s Lon=%s crime_date=%s>" % (crime_type, lat, lon, crime_date)

		f.write(lat + " " +lon + '\n')
	f.close()
	crime_fh.close()

if __name__ == '__main__':

	add_crime_data()