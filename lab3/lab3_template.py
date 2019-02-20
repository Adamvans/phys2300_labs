'''
--------------------------------------------------------------------------------
G e n e r a l I n f o r m a t i o n
--------------------------------------------------------------------------------
Name: weather.py

Usage: python datafile

Description: Code to analyze weather data

Inputs: name of data file containing weather data

Outputs: plots and analysis

Auxiliary Files: None

Special Instructions: None

--------------------------------------------------------------------------------
'''
import sys
import matplotlib.pylab as plt
import numpy as np
import datetime

# Pseudocode:
# 1) get the name of the data file from the user on the command line
# 2) open the data file
# 3) read the first line of data and throw it away (it is the header info the computer doesn't need)
#       from all the remaining lines:
#       read in the date (index 2) and temperature (index 3)
#       parse the date string into year, month, day
#       convert year, month, day into decimal years for plotting
# 4) make two lists for the time series - the decimal year list and the temperature list
# 5) sort the data by month so we can average it and take the standard deviation later
# 6) Plot the results


def parse_data(infile):
    """
    Function to parse weather data
    :param infile: weather data input file
    :return: two lists. One list with the information from the third column (date)
                        One list with the information from the fourth column (temperature)
    """
    wdates = []             # list of dates data
    wtemperatures = []      # list of temperarture data
    years = []               # list of year data. 

    # open file 
    with open(infile, mode="r",) as file:
        # read first line  
        file.readline()
        for line in file:
            # split line with spaces.   
            record = line.rstrip().split()

            # get date info from the line 
            yearDayMonth = record[2]
            year = yearDayMonth[0:4]
            years.append(int(year))
            month = yearDayMonth[4:6]
            day = yearDayMonth[6:8]

            # set the date and append to wdates 
            date = datetime.date(int(year), int(month), int(day))
            wdates.append(date)

            # set the temp and append to wtemperatures
            temp = float(record[3])
            wtemperatures.append(temp)

    return wdates, wtemperatures, years


def calc_mean_std_dev(wdates, wtemp):
    """
    Calculate the mean temperature per month
    Calculate the standard deviation per month's mean
    :param wdates: list with dates fields
    :param wtemp: temperature per month
    :return: means, std_dev: months_mean and std_dev lists
    """

    # list populated so that we can add them so that they are in order.
    means = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    std_dev = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    monthTemps = {}

    # organize the data into a dictionary to group temps by month. 
    for date, temp in zip(wdates, wtemp):
        # create a string key by month 
        month = str(date.month)
        # if key exists add temp to key 
        if month in monthTemps:
            monthTemps[month].append(float(temp))
        # if key dosent exist add key then add temp to key 
        else:
            monthTemps[month] = []
            monthTemps[month].append(float(temp))

    # useing a dicionary get the mean for each month and the standerd devation for each month. 
    for key, value in monthTemps.items():
        intKey = int(key)
        means[intKey - 1] = sum(value)/len(value)
        std_dev[intKey - 1] = np.std(value)

    return means, std_dev



def plot_data_task1(wyear, wtemp, month_mean, month_std):
    """
    Create plot for Task 1.
    :param: wyear: list with year (in decimal)
    :param: wtemp: temperature per
    :param: month_mean: list with month's mean values
    :param: month_std: list with month's mean standard dev values
    """
    # Create canvas with two subplots
    plt.figure()
    plt.subplot(2, 1, 1)                # select first subplot
    plt.title("Temperatures at Ogden")
    plt.plot(wyear, wtemp, "bo")
    plt.ylabel("Temperature, F")
    plt.xlabel("Decimal Year")
    plt.xticks(range(1970,2016, 5)) # set ticks 

    plt.subplot(2, 1, 2)                # select second subplot
    plt.ylabel("Temperature, F")
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthNumber = list(range(1, 13, 1))
    plt.xlim([0.0, 13])
    plt.ylim([0, 90])
    width = 0.8
    plt.bar(monthNumber, month_mean, yerr=month_std, width=width,
            color="lightgreen", ecolor="black", linewidth=1.5)
    plt.xticks(monthNumber, months)
    plt.show()      # display plot


def plot_data_task2(xxx):
    """
    Create plot for Task 2. Describe in here what you are plotting
    Also modify the function to take the params you think you will need
    to plot the requirements.
    :param: xxx??
    """
    pass


def main(infile):
    weather_data = infile    # take data file as input parameter to file
    wdates, wtemperatures, wyear = parse_data(weather_data)
    # Calculate mean and standard dev per month
    month_mean, month_std = calc_mean_std_dev(wdates, wtemperatures)
    # I have a list of:
    #       1) years, 2) temperature, 3) month_mean, 4) month_std
    plot_data_task1(wyear, wtemperatures, month_mean, month_std)
    # TODO: Create the data you need for this
    # plot_data_task2(xxx)



if __name__ == "__main__":
    # infile = 'data/CDO6674605799016.txt'  # for testing
    # Note: the 0th argument is the program itself.
    infile = sys.argv[1]
    main(infile)
    exit(0)
