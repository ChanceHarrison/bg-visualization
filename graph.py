from getData import *
import matplotlib.pyplot as plt
import numpy as np

HIGH_LIMIT = 180
LOW_LIMIT = 70

data = collectData()

# dict = {week1 [high entries, in-range entries, low entries], week2, [...], ...}
weeklyData = {}
weeklyDataPercent = {}

for k in data:
    # Determine what week each entry is in
    date = datetime.fromtimestamp(k / 1000)
    weekNum = datetime.date(date).isocalendar()[1]
    if not weekNum in weeklyData:
        weeklyData[weekNum] = [0, 0, 0]
    else:
        if data[k] > HIGH_LIMIT:
            weeklyData[weekNum][0] += 1
        elif data[k] < LOW_LIMIT:
            weeklyData[weekNum][2] += 1
        elif LOW_LIMIT < data[k] < HIGH_LIMIT:
            weeklyData[weekNum][1] += 1

# Data refinement
for k in list(weeklyData):
    totalEntries = sum(weeklyData[k])
    if totalEntries == 0:
        del weeklyData[k]

for k in weeklyData:
    # totalEntries equals the sum of the list at the key value
    totalEntries = sum(weeklyData[k])
    if not k in weeklyDataPercent:
        weeklyDataPercent[k] = [0, 0, 0]
    for a in range(3):
        weeklyDataPercent[k][a] = weeklyData[k][a]/totalEntries * 100

# Graphing
fig = plt.figure()
width = 0.35

# Bar graph showing percent high/in-range/low for each week

ax1 = fig.add_subplot(111)
highList = []
inRangeList = []
lowList = []

N = len(weeklyDataPercent)
ind = np.arange(N)

weeklyDataPercentValues = list(weeklyDataPercent.values())
weeklyDataPercentKeys = list(weeklyDataPercent.keys())

for i in range(len(weeklyDataPercentValues)):
    highList.append(weeklyDataPercentValues[i][0])
    inRangeList.append(weeklyDataPercentValues[i][1])
    lowList.append(weeklyDataPercentValues[i][2])

low = ax1.bar(range(len(weeklyDataPercent)), lowList, align='center', color='#d60000')
inRange = ax1.bar(range(len(weeklyDataPercent)), inRangeList, align='center', color='#01c61f', bottom=lowList)
high = ax1.bar(range(len(weeklyDataPercent)), highList, align='center', color='#ffee02', bottom=inRangeList)

ax1.set(title="Time in range by week", ylabel="Percent", xlabel="Week")

axes = plt.gca()
axes.set_ylim([0, 100])

plt.legend((high[0], inRange[0], low[0]), ("High", "In-range", "Low"), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xticks(ind, weeklyDataPercentKeys)
plt.show()
