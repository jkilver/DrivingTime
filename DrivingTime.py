# Get the driving time so I can find the best time to drive to work

import simplejson, urllib
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import time
import calendar

def SavePlot(sample_times, driving_times):
    # Create the dataframe
    df = pd.DataFrame(driving_times, index=sample_times, columns=['driving time (minutes)'] )

    # Plot the dataframe
    df.plot()

    # Create file name
    title = calendar.day_name[dt.date.today().weekday() - 1]
    filename = '.\\Plots\\' + title + '.png'

    # Save the figure
    plt.savefig(filename)


if __name__ == "__main__":

    # Set up the coordinates
    orig_lat = 42.908594
    orig_lng = -82.989267 
    dest_lat = 42.515091 
    dest_lng = -83.040376

    # Generate the url
    url = "http://maps.googleapis.com/maps/api/distancematrix/json?origins={0},{1}&destinations={2},{3}&mode=driving&language=en-EN&sensor=false".format(str(orig_lat),str(orig_lng),str(dest_lat),str(dest_lng))

    # Allocate the arrays
    sample_times = []
    driving_times = []

    prev_time = dt.datetime.now()

    while True:
        # Get the current date and time
        current = dt.datetime.now()
        sample_times.append(current)

        # Get the response from Google
        result= simplejson.load(urllib.urlopen(url))

        # Add the driving time to the list
        driving_time = result['rows'][0]['elements'][0]['duration']['value']/60.0
        driving_times.append(driving_time)

        # Determine if we need to switch the data sets over and save off the plots
        if current.day != prev_time.day:
            SavePlot(sample_times, driving_times)
            sample_times[:] = []
            driving_times[:] = []

        # Wait 5 minutes
        time.sleep(5)