# Import the functions from getData (allowing their use without the 'getData.' prefix)
from getData import *
import matplotlib.pyplot as plt
import numpy as np

# Constants to determine whether any given BG value is considered high or low (and by extension, in-range)
HIGH_LIMIT = 180
LOW_LIMIT = 70

# Set data equal to results from the collectData() function in the getData.py script
data = collectData()

# format: {week1 [high entries, in-range entries, low entries], week2, [...], ...}
weeklyData = {}
weeklyDataPercent = {}

for k in data:
    # By getting a full date from a ms since epoch timestamp...
    date = datetime.fromtimestamp(k / 1000)
    # ...it is possible to find what week of the year each entry is in
    weekNum = datetime.date(date).isocalendar()[1]

    # If any given week isn't already included in the data dictionary...
    if not weekNum in weeklyData:
        # ...then set the value for the weekNum key to be a list with 3 elements
        weeklyData[weekNum] = [0, 0, 0]
    # TODO: The above statement unintentionally discards the first entry
    # If the week already exists in the dictionary...
    else:
        # ...then determine whether the BG value is high/low/in-range and increment the proper list element
        if data[k] > HIGH_LIMIT:
            weeklyData[weekNum][0] += 1
        elif data[k] < LOW_LIMIT:
            weeklyData[weekNum][2] += 1
        elif LOW_LIMIT < data[k] < HIGH_LIMIT:
            weeklyData[weekNum][1] += 1

# Data refinement

# Delete any empty entries
for k in list(weeklyData):
    totalEntries = sum(weeklyData[k])
    if totalEntries == 0:
        del weeklyData[k]

# Convert the entries of each type to a percentage of the total entries
for k in weeklyData:
    # totalEntries equals the sum of the list at the key value
    totalEntries = sum(weeklyData[k])
    if not k in weeklyDataPercent:
        weeklyDataPercent[k] = [0, 0, 0]
    for a in range(3):
        weeklyDataPercent[k][a] = weeklyData[k][a]/totalEntries * 100

# Graphing: (Stacked) bar graph showing percent high/in-range/low for each week

# Create a figure
fig = plt.figure()

# Add a subplot (create axes)
ax1 = fig.add_subplot(111)

# Create empty lists to store all high/in-range/low percentages
highList = []
inRangeList = []
lowList = []

# Create and store lists for the values and keys of the weeklyDataPercent dictionaries
weeklyDataPercentValues = list(weeklyDataPercent.values())
weeklyDataPercentKeys = list(weeklyDataPercent.keys())

# Iterate through the weeklyDataPercentValues dictionary to populate the empty lists above
for i in range(len(weeklyDataPercentValues)):
    highList.append(weeklyDataPercentValues[i][0])
    inRangeList.append(weeklyDataPercentValues[i][1])
    lowList.append(weeklyDataPercentValues[i][2])

# Create the bars and stack them on top of each other
low = ax1.bar(range(len(weeklyDataPercent)), lowList, align='center', color='#d60000')
inRange = ax1.bar(range(len(weeklyDataPercent)), inRangeList, align='center', color='#01c61f', bottom=lowList)
high = ax1.bar(range(len(weeklyDataPercent)), highList, align='center', color='#ffee02', bottom=inRangeList)

# Set graph title and labels for each axis
ax1.set(title="Time in range by week", ylabel="Percent", xlabel="Week")

# Get the current axes and set the limits of the y-axis from 0 to 100
axes = plt.gca()
axes.set_ylim([0, 100])

# Create a legend for the figure in the upper right
plt.legend((high[0], inRange[0], low[0]), ("High", "In-range", "Low"), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

# Use the numpy package to facilitate the creation of x ticks on the figure
N = len(weeklyDataPercent)
ind = np.arange(N)

# Create x ticks for each bar
plt.xticks(ind, weeklyDataPercentKeys)

# Show the figure
plt.show()
