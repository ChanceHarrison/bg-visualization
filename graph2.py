from getData import *
import matplotlib.pyplot as plt
import numpy as np

HIGH_LIMIT = 180
LOW_LIMIT = 70

data = collectData()

# dict = {monday [high, in-range, low], tuesday [...], ...}
dailyData = {}
dailyDataPercent = {}

for k in data:
    date = datetime.fromtimestamp(k / 1000)
    dayNum = date.weekday()
    if not dayNum in dailyData:
        dailyData[dayNum] = [0, 0, 0]
    else:
        if data[k] > HIGH_LIMIT:
            dailyData[dayNum][0] += 1
        elif data[k] < LOW_LIMIT:
            dailyData[dayNum][2] += 1
        elif LOW_LIMIT < data[k] < HIGH_LIMIT:
            dailyData[dayNum][1] += 1

for k in list(dailyData):
    totalEntries = sum(dailyData[k])
    if totalEntries == 0:
        del dailyData[k]

for k in dailyData:
    # totalEntries equals the sum of the list at the key value
    totalEntries = sum(dailyData[k])
    if not k in dailyDataPercent:
        dailyDataPercent[k] = [0, 0, 0]
    for a in range(3):
        dailyDataPercent[k][a] = dailyData[k][a]/totalEntries * 100

# Graphing: (Stacked) bar graph showing the percent high/in-range/low for each day of the week
fig = plt.figure()
width = 0.3

ax2 = fig.add_subplot(111)

highList2 = []
inRangeList2 = []
lowList2 = []

dailyDataPercentValues = list(dailyDataPercent.values())

for i in range(len(dailyDataPercentValues)):
    highList2.append(dailyDataPercentValues[i][0])
    inRangeList2.append(dailyDataPercentValues[i][1])
    lowList2.append(dailyDataPercentValues[i][2])

low = ax2.bar(range(len(dailyDataPercent)), lowList2, width, align='center', color='#d60000')
inRange = ax2.bar(range(len(dailyDataPercent)), inRangeList2, width, align='center', color='#01c61f', bottom=lowList2)
high = ax2.bar(range(len(dailyDataPercent)), highList2, width, align='center', color='#ffee02', bottom=inRangeList2)

ax2.set(title="Time in range by weekday", ylabel="Percent", xlabel="Day")

axes = plt.gca()
axes.set_ylim([0, 100])

plt.legend((high[0], inRange[0], low[0]), ("High", "In-range", "Low"), bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

N = 7
ind = np.arange(N)

plt.xticks(ind, ('Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat', 'Sun'))
plt.show()
