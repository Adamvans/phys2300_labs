'''
Assignment to learn how to interpolate data1
'''
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as md
import datetime
import numpy as np
# import scipy
import pandas as pd


def read_wx_data(wx_file, harbor_data):
    """
    Read temperature and time data from file.
    Populates the harbor_data dictionary with two lists: wx_times and wx_temperatures
    :param wx_file: File object with data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    TempData = pd.read_csv(wx_file)

    # remove unneeded columns. 
    del TempData['Date']
    del TempData['millisecs']
    del TempData['Ch2:Deg F']
    del TempData['Ch3:']
    del TempData['Ch4:Deg F']

    # turn time and altitude into a dict. 
    TempDict = {}
    TempDict['Temperature'] = TempData['Ch1:Deg F'].tolist()
    TempDict['Time'] = TempData['Time'].tolist()

    # add data to harbor_data dict. 
    harbor_data.update(TempDict)
    
   
    


def read_gps_data(gps_file, harbor_data):
    """
    Read gps and altitude data from file.
    Populates the harbor_data dictionary with two lists: gps_times and gps_altitude
    :param gps_file: File object with gps data
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    # pull data from file. delimiter for coloumn names is 2 or more spaces, delimitor for data is tabs. 
    # skip first row which is a line if dashes 
    GPSData = pd.read_csv(gps_file, sep='[\s]{2,}|\t', skiprows=[1], engine='python')
    
    # remove unneeded columns. 
    del GPSData['MET (MIN)']
    del GPSData['LAT (decimal deg)']
    del GPSData['LONG (decimal deg)']

    # change time zone from gmt to mst
    GPSData['GPS HOURS'] = GPSData['GPS HOURS'].map(int) - 6

    # merge time cloumns into one column  
    GPSData['GPS Time'] = GPSData['GPS HOURS'].map(str) +":"+ GPSData['MIN'].map(str) +":"+ GPSData['SEC'].map(str)

    # remove old time columns.
    del GPSData['GPS HOURS']
    del GPSData['MIN']
    del GPSData['SEC']

    # turn time and altitude into a dict. 
    GPSDict = {}
    GPSDict['GPSTime'] = GPSData['GPS Time'].tolist()
    GPSDict['Altitude'] = GPSData['ALT (ft)'].tolist()

    # add data to harbor_data dict. 
    harbor_data.update(GPSDict)
    


def interpolate_wx_from_gps(harbor_data):
    """
    Compute wx altitudes by interpolating from gps altitudes
    Populates the harbor_data dictionary with three lists:
        1) wx correlated tinme 
        2) wx correlated temperature
        3) wx correlated altitude
    :param harbor_data: A dictionary to collect data.
    :return: Nothing
    """
    #create three lists of the same size that match by index. the time list will use date times. 
    wx_temperatures = np.array([] , int)
    wx_times = np.array([], dtype = 'datetime64[s]')
    wx_altitude = np.array([], int)
    #set a first instance of last time starting at 0 
    lastTime = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
    #set a first instance of last altitude starting at 0 
    LastAlt = 0 
    #set a loop to loop though the ttemoerature list to match up the times on the temp list to the gpslist.  
    loop = 0
    #loop thourogh the gpslist to start populating the three new lists. 
    for AltValue ,Timevalue in zip( harbor_data['Altitude'], harbor_data['GPSTime']):

        #set a this time varable to use the gpstime to match the temp time 
        thisTime = datetime.datetime.strptime(Timevalue, '%H:%M:%S')
        #set a temp time varable to use the temprature time to match the gps time
        tempTime = datetime.datetime.strptime(harbor_data['Time'][loop], '%H:%M:%S')
        #set a  temperature to get the temp that corrasponds to temp time 
        temperature = harbor_data['Temperature'][loop]
        
        #get the slope of the line by getting the change of both altitude and time 
        AltChange = AltValue - LastAlt
        TimeChange = thisTime - lastTime

        #loop though the tempature lists to match up to the gps time.  
        while(tempTime < thisTime):
            #if this is the tempratures before the first gps reading dont record them. 
            if(datetime.datetime.strptime('00:00:00', '%H:%M:%S') < lastTime):
                #get the precentage of change between this gpstime and last gpstime 
                delta = (tempTime - lastTime)/ TimeChange
                #change the altitude by the same persentage so that the point sits on the same line 
                corrAlt = delta*AltChange + LastAlt
                
                #add all three datapoints at the same time so that the time is for both altitue and temp. 
                wx_altitude = np.append(wx_altitude, corrAlt)
                wx_times = np.append(wx_times, tempTime)
                wx_temperatures = np.append(wx_temperatures, temperature)

            # increment loop and get new tempreature time and tempreature data 
            loop = loop + 1
            tempTime = datetime.datetime.strptime(harbor_data['Time'][loop], '%H:%M:%S')
            temperature = harbor_data['Temperature'][loop]
        
        # get last temp time so that we can have both temps on ether side of the gps reading 
        lastTempTime = datetime.datetime.strptime(harbor_data['Time'][loop - 1], '%H:%M:%S')

        #get the slope of the line by getting the change of both tempreature and time 
        TimeChange = (tempTime - lastTempTime)
        tempChange = (harbor_data['Temperature'][loop] - harbor_data['Temperature'][loop - 1])

        #get the precentage of change between this temptime and last temptime
        delta = (thisTime - lastTempTime)/ TimeChange

        #change the tempreature by the same persentage so that the point sits on the same line 
        corrTemp = delta*tempChange +  harbor_data['Temperature'][loop - 1]
        
        #dont do the first time do stop duplacation  
        if(datetime.datetime.strptime('00:00:00', '%H:%M:%S') < lastTime):

            #add all three datapoints at the same time so that the time is for both altitue and temp. 
            wx_altitude = np.append(wx_altitude, AltValue)
            wx_times = np.append(wx_times, thisTime)
            wx_temperatures = np.append(wx_temperatures, corrTemp)

        # increment data on the for loop. 
        lastTime = thisTime 
        LastAlt = AltValue
    
    # add all data in lists to harbor_data dict. 
    CorrDict = {}
    CorrDict['CorrTemperatures'] = wx_temperatures.tolist()
    CorrDict['CorrTimes'] = wx_times.tolist()
    CorrDict['CorrAltitudes'] = wx_altitude.tolist()

    harbor_data.update(CorrDict)


def plot_figs(harbor_data):
    """
    Plot 2 figures with 2 subplots each.
    :param harbor_data: A dictionary to collect data.
    :return: nothing
    """
    # format date for x-axis so it only shows time 
    xformatter = md.DateFormatter('%H:%M')
    # create first figure 
    plt.figure(1)
    # Create canvas with two subplots
    plt.subplot(2, 1, 1)                # select first subplot
    plt.title("Temperatures for mission")
    # plot time and Temperature
    plt.plot(harbor_data['CorrTimes'], harbor_data['CorrTemperatures'])
    plt.ylabel("Temperature, F")
    # format date with formater 
    plt.gca().xaxis.set_major_formatter(xformatter)
    

    plt.subplot(2, 1, 2)                # select second subplot
    plt.title("Altitude of mission")
    # plot time and Altitude
    plt.plot(harbor_data['CorrTimes'], harbor_data['CorrAltitudes']) 
    plt.ylabel("Altitude")
    plt.xlabel("Misstion Time")
    # format date with formater 
    plt.gca().xaxis.set_major_formatter(xformatter)
    
    # get the max number for assending and desending 
    max_index = harbor_data['CorrAltitudes'].index(max(harbor_data['CorrAltitudes']))
    # get altitude and temp list for assending by making a new list with everthing before max and include max with + 1 
    assentAlt = harbor_data['CorrAltitudes'][:max_index + 1]
    assentTemp = harbor_data['CorrTemperatures'][:max_index + 1]
    # get altitude and temp list for decending by making a new list with everthing after max and include max with -1
    desentAlt = harbor_data['CorrAltitudes'][max_index - 1:]
    desentTemp = harbor_data['CorrTemperatures'][max_index - 1:]

    # Create second canvas with two subplots
    plt.figure(2)
    plt.subplot(1, 2, 1)    # select first subplot
    plt.title("Assent")
    plt.plot(assentTemp , assentAlt)
    plt.ylabel("Altitude")
    plt.xlabel("Temperature, F")

    plt.subplot(1, 2, 2)  # select second subplot
    plt.title("Desent")
    plt.plot(desentTemp , desentAlt)
    plt.xlabel("Temperature, F")

    plt.show()      # display plots

def main():
    """
    Main function
    :return: Nothing
    """
    harbor_data = {}
    wx_file = sys.argv[1]                   # first program input param
    gps_file = sys.argv[2]                  # second program input param

    read_wx_data(wx_file, harbor_data)      # collect weather data
    read_gps_data(gps_file, harbor_data)    # collect gps data
    interpolate_wx_from_gps(harbor_data)    # calculate interpolated data
    plot_figs(harbor_data)                  # display figures


if __name__ == '__main__':
    main()
    exit(0)
