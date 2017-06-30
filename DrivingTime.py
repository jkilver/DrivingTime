# Get the driving time so I can find the best time to drive to work

import simplejson, urllib
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import time
import calendar
import numpy as np

def SavePlot(sample_times, to_work, from_work):
    # Create the dataframe
    driving_times = np.array([ to_work, from_work ]).transpose()

    df = pd.DataFrame(driving_times, index=sample_times, columns=['driving time to work (minutes)', 'driving time from work (minutes)'] )

    # Plot the dataframe
    df.plot()

    # Create file name
    title = calendar.day_name[dt.date.today().weekday() - 1]
    filename = '.\\Plots\\' + title + '.png'

    print 'Saving ' + filename

    # Save the figure
    plt.savefig(filename)


if __name__ == "__main__":

    # Set up the coordinates
    orig_lat = 42.908594
    orig_lng = -82.989267 
    dest_lat = 42.515091 
    dest_lng = -83.040376

    # API Key
    # AIzaSyDwGmIteahxi5ixK0P2aL055lIzhnMgvHA 

    # Generate the url
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations={2},{3}&mode=driving&language=en-EN&sensor=false".format(str(orig_lat),str(orig_lng),str(dest_lat),str(dest_lng))
    url_to_work = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=8929+Hough+Road+Almont+MI&destinations=Warren+Technical+Center&departure_time=now&key=AIzaSyDwGmIteahxi5ixK0P2aL055lIzhnMgvHA"
    url_from_work = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=Warren+Technical+Center&destinations=8929+Hough+Road+Almont+MI&departure_time=now&key=AIzaSyDwGmIteahxi5ixK0P2aL055lIzhnMgvHA"
    
    # Allocate the arrays
    sample_times = []
    times_to_work = []
    times_from_work = []

    prev_time = dt.datetime.now()

    while True:
        # Get the current date and time
        current = dt.datetime.now()
        sample_times.append(current)

        # Get the response from Google
        result_to_work = simplejson.load(urllib.urlopen(url_to_work))
        result_from_work  = simplejson.load(urllib.urlopen(url_from_work))

        # Add the driving time to the list
        time_to_work = result_to_work['rows'][0]['elements'][0]['duration_in_traffic']['value']/60.0
        time_from_work = result_from_work['rows'][0]['elements'][0]['duration_in_traffic']['value']/60.0
        times_to_work.append(time_to_work)
        times_from_work.append(time_from_work)
        print "At time " + str(current) + " driving time to work is " + str(time_to_work) + " minutes. Driving time from work is " + str(time_from_work)

        # Determine if we need to switch the data sets over and save off the plots
        if current.day != prev_time.day:
            SavePlot(sample_times, times_to_work, times_from_work)
            sample_times[:] = []
            times_to_work[:] = []
            times_from_work[:] = []

        # Update the previous time variable  
        prev_time = current

        # Wait 5 minutes
        time.sleep(300)