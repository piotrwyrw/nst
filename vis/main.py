import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import json
import datetime as dt

xpoints = []
upValues = []
downValues = []
averagesDown = []
averagesUp = []
averagesPing = []
pings = []

try:
    results = open('speed_results.json')
except FileNotFoundError:
    print('Failed to open results file: speed_results.json')
    exit(0)

jsonData = json.load(results)

firstUnix = 0

sumUp = 0
sumDown = 0
sumPing = 0
sumCount = 0

resultsArr = jsonData['results']
for entry in resultsArr:
    if firstUnix == 0:
        firstUnix = entry['unix']

    sumCount += 1

    # +2 Hours --> CEST
    xpoints.append(dt.datetime.utcfromtimestamp(entry['unix']) + dt.timedelta(hours=2))

    upValues.append(entry['up'])
    sumUp = sumUp + entry['up']
    averagesUp.append(sumUp / sumCount)

    pings.append(entry['ping'])
    sumPing = sumPing + entry['ping']
    averagesPing.append(sumPing / sumCount)

    downValues.append(entry['down'])
    sumDown = sumDown + entry['down']
    averagesDown.append(sumDown / sumCount)


avgUp = sumUp / sumCount
avgDown = sumDown / sumCount
avgPing = sumPing / sumCount

points_x = np.array(xpoints)
points_up = np.array(upValues)
points_down = np.array(downValues)
points_averagesDown = np.array(averagesDown)
points_averagesUp = np.array(averagesUp)
points_averagesPing = np.array(averagesPing)
points_pings = np.array(pings)

labelUp = 'Upload'
labelDown = 'Download'
labelPing = 'Ping'
labelUpAvg = 'Upload Avg. ({} Mb/s)'.format(round(avgUp, 1))
labelDownAvg = 'Download Avg. ({} Mb/s)'.format(round(avgDown, 1))
labelPingAvg = 'Ping Avg. ({} ms)'.format(round(avgPing))

fig, axs = plt.subplots(3)

fig.set_size_inches(10,7)
fig.suptitle('NST v3.2, {} Samples'.format(points_x.size))

def scatter():
    axs[0].scatter(points_x, points_up, color='mediumblue', label=labelUp, s=1)
    axs[0].scatter(points_x, points_down, color='mediumseagreen', label=labelDown, s=1)
    axs[1].scatter(points_x, points_averagesDown, color='mediumseagreen', label=labelDownAvg, s=1)
    axs[1].scatter(points_x, points_averagesUp, color='mediumblue', label=labelUpAvg, s=1)
    axs[2].scatter(points_x, points_pings, color='orange', label=labelPing, s=1)
    axs[2].scatter(points_x, points_averagesPing, color='darkorange', label=labelPingAvg, s=1.5)


def plot():
    axs[0].plot(points_x, points_up, color='mediumblue', label=labelUp, linewidth=0.5)
    axs[0].plot(points_x, points_down, color='mediumseagreen', label=labelDown, linewidth=0.5)
    axs[1].plot(points_x, points_averagesDown, color='mediumseagreen', label=labelDownAvg, linewidth=0.5)
    axs[1].plot(points_x, points_averagesUp, color='mediumblue', label=labelUpAvg, linewidth=0.5)
    axs[2].plot(points_x, points_pings, color='orange', label=labelPing, linewidth=0.5)
    axs[2].plot(points_x, points_averagesPing, color='darkorange', label=labelPingAvg, linewidth=1)


def saveAndShow(fname):

    for ax in axs:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    axs[0].legend()
    axs[1].legend()
    axs[2].legend()
    plt.savefig(fname + '.pdf')
    plt.savefig(fname + '.png', dpi=500)


scatter()
saveAndShow('speed_scatter')
axs[0].cla()
axs[1].cla()
axs[2].cla()
plot()
saveAndShow('speed_plot')
