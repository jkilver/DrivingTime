# Get the driving time so I can find the best time to drive to work

import simplejson, urllib
orig_lat = 42.908594
orig_lng = -82.989267 
dest_lat = 42.515091 
dest_lng = -83.040376
orig_coord = orig_lat,orig_lng
dest_coord = dest_lat,dest_lng
url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations={2},{3}&mode=driving&language=en-EN&sensor=false".format(str(orig_lat),str(orig_lng),str(dest_lat),str(dest_lng))
print url
result= simplejson.load(urllib.urlopen(url))
driving_time = result['rows'][0]['elements'][0]['duration']['value']
print driving_time/60.0