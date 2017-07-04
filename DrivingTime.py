# Get the driving time so I can find the best time to drive to work

import simplejson, urllib
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import time
import calendar
import numpy as np
import sys

def SavePlot(sample_times, to_work, from_work):
    # Create the dataframe
    driving_times = np.array([ to_work, from_work ]).transpose()
    
    df = pd.DataFrame(driving_times, index=sample_times, columns=[ 'To work (min)', 'From work (min)'] )

    # Plot the dataframe
    df.plot()

    # Create file name
    title = dt.date.today()
    filename = '.\\Plots\\' + title + '.png'

    print 'Saving ' + filename

    # Save the figure
    plt.savefig(filename)
    df.to_csv('.\\Files\\' + title + '.csv')


if __name__ == "__main__":

    # API Key
    # AIzaSyDwGmIteahxi5ixK0P2aL055lIzhnMgvHA 

    # Generate the url
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

        # Determine if we need to switch the data sets over
        if current.day != prev_time.day:   
            sample_times[:] = []
            times_to_work[:] = []
            times_from_work[:] = []

        # Get the response from Google
        result_to_work = simplejson.load(urllib.urlopen(url_to_work))
        result_from_work  = simplejson.load(urllib.urlopen(url_from_work))

        # Add the driving time to the list
        try:
            time_to_work = result_to_work['rows'][0]['elements'][0]['duration_in_traffic']['value']/60.0
            time_from_work = result_from_work['rows'][0]['elements'][0]['duration_in_traffic']['value']/60.0

            times_to_work.append(time_to_work)
            times_from_work.append(time_from_work)
            print "At time " + str(current) + " driving time to work is " + str(time_to_work) + " minutes. Driving time from work is " + str(time_from_work)
        except:
            e = sys.exc_info()[0]
            print "Error getting travel time: ", e
            
        # Update plot
        if len(sample_times) >= 2:
            SavePlot(sample_times, times_to_work, times_from_work)

        # Update the previous time variable  
        prev_time = current

        # Wait 5 minutes
        time.sleep(300)