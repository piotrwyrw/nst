import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import json
import datetime as dt

# ---------- Configuration section ----------
average_smooth_samples = 25

xpoints = []
upValues = []
downValues = []
averagesDown = []
averagesUp = []
averagesPing = []
pings = []

# Sweep from 0 to 20KHz
try:
    results = open('speed_results.json')
except FileNotFoundError:
    print('Failed to open results file: speed_results.json')
    exit(0)

jsonData = json.load(results)

sumUp = 0
sumDown = 0
sumPing = 0
sumCount = 0


def average(samples, org, arr):
    # Negative sample count is not supported
    if samples < 0:
        return 0.0

    # Origin index is way out of bounds
    if org > len(arr) or org < 0:
        return 0.0

    # We cannot take the requested amount of samples
    if org + samples >= len(arr):
        # How many samples can we take?
        rem_samples = len(arr) - org - 1

        # Take the remaining amount of samples
        if rem_samples > 0:
            return average(rem_samples, org, arr)

        # If this is the last index, just return the actual value from the array at that point
        return arr[org]

    # However, if it is possible to take the requested amount of samples, we shall do so.
    sum = 0

    for idx in range(org, org + samples):
        sum += arr[idx]

    # Turn the sum into an average
    avg = sum / samples

    return avg


resultsArr = jsonData['results']
for i, entry in enumerate(resultsArr):
    sumCount += 1

    xpoints.append(dt.datetime.utcfromtimestamp(entry['unix']) + dt.timedelta(hours=2))

    upValues.append(entry['up'])
    sumUp = sumUp + entry['up']
    # averagesUp.append(sumUp / sumCount)

    pings.append(entry['ping'])
    sumPing = sumPing + entry['ping']
    # averagesPing.append(sumPing / sumCount)

    downValues.append(entry['down'])
    sumDown = sumDown + entry['down']
    # averagesDown.append(sumDown / sumCount)

# Compute the final averages for use on the legend
avgUp = sumUp / sumCount
avgDown = sumDown / sumCount
avgPing = sumPing / sumCount

# Compute the local averages
for i in range(len(xpoints)):
    # For every X-point, compute the local average and add it to the averages array
    averagesUp.append(average(average_smooth_samples, i, upValues))
    averagesDown.append(average(average_smooth_samples, i, downValues))
    averagesPing.append(average(average_smooth_samples, i, pings))

# Convert to numpy arrays
points_x = np.array(xpoints)
points_up = np.array(upValues)
points_down = np.array(downValues)
points_averagesDown = np.array(averagesDown)
points_averagesUp = np.array(averagesUp)
points_averagesPing = np.array(averagesPing)
points_pings = np.array(pings)

# The aforementioned legend labels
labelUp = 'Upload'
labelDown = 'Download'
labelPing = 'Ping'
labelUpAvg = 'Upload Avg. ({} Mb/s) $\leq$ {}'.format(round(avgUp, 1), round(max(points_averagesUp)))
labelDownAvg = 'Download Avg. ({} Mb/s) $\leq$ {}'.format(round(avgDown, 1), round(max(points_averagesDown)))
labelPingAvg = 'Ping Avg. ({} ms) $\geq$ {}'.format(round(avgPing), round(min(points_averagesPing)))

fig, axs = plt.subplots(3)

fig.set_size_inches(10, 6)
fig.suptitle('Internet speed fluctuation over time'.format(points_x.size))


def scatter():
    axs[0].scatter(points_x, points_up, color='mediumblue', label=labelUp, s=1)
    axs[0].scatter(points_x, points_down, color='mediumseagreen', label=labelDown, s=1)
    axs[1].scatter(points_x, points_averagesDown, color='mediumseagreen', label=labelDownAvg, s=1)
    axs[1].scatter(points_x, points_averagesUp, color='mediumblue', label=labelUpAvg, s=1)
    axs[2].scatter(points_x, points_pings, color='orange', label=labelPing, s=1)
    axs[2].scatter(points_x, points_averagesPing, color='red', label=labelPingAvg, s=1.5)


def plot():
    axs[0].plot(points_x, points_up, color='mediumblue', label=labelUp, linewidth=0.5)
    axs[0].plot(points_x, points_down, color='mediumseagreen', label=labelDown, linewidth=0.5)
    axs[1].plot(points_x, points_averagesDown, color='mediumseagreen', label=labelDownAvg, linewidth=0.5)
    axs[1].plot(points_x, points_averagesUp, color='mediumblue', label=labelUpAvg, linewidth=0.5)
    axs[2].plot(points_x, points_pings, color='orange', label=labelPing, linewidth=0.5)
    axs[2].plot(points_x, points_averagesPing, color='red', label=labelPingAvg, linewidth=1)


def save_and_show(fname):
    for ax in axs:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    axs[0].legend()
    axs[1].legend()
    axs[2].legend()
    plt.savefig(fname + '.pdf')
    plt.savefig(fname + '.png', dpi=500)


scatter()
save_and_show('speed_scatter')
axs[0].cla()
axs[1].cla()
axs[2].cla()
plot()
save_and_show('speed_plot')
