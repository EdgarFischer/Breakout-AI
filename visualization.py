import matplotlib.pyplot as plt

# Data for Bricks1
bricks1_onp = [-58.97058824, -65.79411765, -53.35294118, -65.82352941, -65.29411765]
bricks1_offp = [-50, -50, -50, -58, -50]
bricks1_esmc_1m = [-61.27272727272727, -107.0, -50.0, -163.1, -83.6]
bricks1_esmc_10m = [-59.0, -60.18181818181818, -52.90909090909091, -58.0, -59.0]

# Data for Bricks2
bricks2_onp = [-57.76470588, -53.11764706, -53.52941176, -47.29411765, -57.58823529]
bricks2_offp = [-44, -54, -48, -41, -44]
bricks2_esmc_1m = [-57.666666666666664, -180.55555555555554, -125.5, -157.35294117647058, -57.470588235294116]
bricks2_esmc_10m = [-51.30769230769231, -124.07692307692308, -48.666666666666664, -41.0, -50.583333333333336]

# Data for Bricks3
bricks3_onp = [-261, -83.36666667, -87.73333333, -90.66666667, -261]
bricks3_offp = [-96, -92, -88, -78, -85]
bricks3_esmc_1m = [-232.45454545454547, -107.0, -190.0, -104.0, -192.6]
bricks3_esmc_10m = [-164.33333333333334, -80.0, -156.9090909090909, -80.0, -152.1818181818182]

# X-axis values (speeds)
speeds = [-2, -1, 0, 1, 2]

# Create a scatter plot for Bricks1
plt.figure(figsize=(10, 6))
plt.scatter(speeds, bricks1_onp, marker='o', label='On-Policy Episilon = 0.02')
plt.scatter(speeds, bricks1_offp, marker='o', label='Off-Policy Random Behavior Policy')
plt.scatter(speeds, bricks1_esmc_1m, marker='o', label='Exploring Starts 1M episodes')
plt.scatter(speeds, bricks1_esmc_10m, marker='o', label='Exploring Starts 10M episodes')
plt.xlabel('Speeds')
plt.ylabel('Average Number Of Moves To Win')
plt.title('Bricks1: Algorithm Comparison')
plt.legend()
plt.grid(True)
plt.xticks(speeds)
plt.ylim(-300, 0)
plt.savefig('bricks1_plot.png')
plt.show()

# Create a scatter plot for Bricks2
plt.figure(figsize=(10, 6))
plt.scatter(speeds, bricks2_onp, marker='o', label='On-Policy Episilon = 0.02')
plt.scatter(speeds, bricks2_offp, marker='o', label='Off-Policy Random Behavior Policy')
plt.scatter(speeds, bricks2_esmc_1m, marker='o', label='Exploring Starts 1M episodes')
plt.scatter(speeds, bricks2_esmc_10m, marker='o', label='Exploring Starts 10M episodes')
plt.xlabel('Speeds')
plt.ylabel('Average Number Of Moves To Win')
plt.title('Bricks2: Algorithm Comparison')
plt.legend()
plt.grid(True)
plt.xticks(speeds)
plt.ylim(-300, 0)
plt.savefig('bricks2_plot.png')
plt.show()

# Create a scatter plot for Bricks3
plt.figure(figsize=(10, 6))
plt.scatter(speeds, bricks3_onp, marker='o', label='On-Policy Episilon = 0.02')
plt.scatter(speeds, bricks3_offp, marker='o', label='Off-Policy Random Behavior Policy')
plt.scatter(speeds, bricks3_esmc_1m, marker='o', label='Exploring Starts 1M episodes')
plt.scatter(speeds, bricks3_esmc_10m, marker='o', label='Exploring Starts 10M episodes')
plt.xlabel('Speeds')
plt.ylabel('Average Number Of Moves To Win')
plt.title('Bricks3: Algorithm Comparison')
plt.legend()
plt.grid(True)
plt.xticks(speeds)
plt.ylim(-300, 0)
plt.savefig('bricks3_plot.png')
plt.show()
