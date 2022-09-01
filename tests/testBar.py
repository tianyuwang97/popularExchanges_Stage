
from matplotlib import pyplot

barWidth = 0.1
y1 = [0, 0, 3, 9]
y2 = [99, 245, 401, 635]
y3 =[2440,2505,2452,2299]
y4 =[2539,2763,2857,2933]

r1 = range(len(y1))
r2 = [x + barWidth for x in r1]
r3 = [x + barWidth for x in r2]
r4 = [x + barWidth for x in r3]


pyplot.bar(r1, y1, width = barWidth, color = ['yellow' for i in y1],)
pyplot.bar(r2, y2, width = barWidth, color = ['pink' for i in y2])
pyplot.bar(r3, y3, width = barWidth, color = ['red' for i in y3])
pyplot.bar(r4, y4, width = barWidth, color = ['blue' for i in y4])
pyplot.xticks([r + barWidth / 2 for r in range(len(y1))], ['A', 'B', 'C', 'D'])

pyplot.show()