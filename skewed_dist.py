from scipy.stats import skewnorm
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

mean = 2.7
std = 1.65

a = 1
b = 7

# normal distribution
x = np.linspace(0, 10, 1000)
y = scipy.stats.norm.pdf(x, mean, std)

plt.figure(figsize=(12, 5))
plt.suptitle("normal vs. truncnorm distribution curve for num_signs", fontsize=16)
plt.subplot(1, 2, 1)
plt.plot(x, y, 'orange', linewidth=3)

_, max_ylim = plt.ylim()
plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
plt.text(mean*1.1, max_ylim*0.95, 'Mean: {:.2f}'.format(mean))

plt.title("num_signs normal distribution")
plt.xlabel("num_signs")
plt.ylabel("probability density")

# truncated normal distribution
y2 = scipy.stats.truncnorm.pdf(x, (a-mean)/std, (b-mean)/std, mean, std)

plt.subplot(1, 2, 2)
plt.plot(x, y2, linewidth=3)

_, max_ylim = plt.ylim()
plt.axvline(mean, color='k', linestyle='dashed', linewidth=1)
if mean > 4:
    plt.text(mean - 2.2, max_ylim * 0.95, 'Mean: {:.2f}'.format(mean))
else:
    plt.text(mean * 1.2, max_ylim * 0.95, 'Mean: {:.2f}'.format(mean))


plt.axvline(a, color='k', linestyle='dashed', linewidth=1)
plt.text(a-1.12, max_ylim*0.95, 'Min: {}'.format(a))

plt.axvline(b, color='k', linestyle='dashed', linewidth=1)
plt.text(b+0.1, max_ylim*0.95, 'Max: {}'.format(b))

plt.title("num_signs truncnorm distribution")
plt.xlabel("num_signs")
plt.ylabel("probability density")


plt.show()

