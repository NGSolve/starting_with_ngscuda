import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt('timing_copyvec.txt', usecols=(0, 1))



sizes, GFlops = zip(*data)

plt.figure(figsize=(8,6))
plt.plot(sizes, GFlops, marker='o', linestyle='-', color='b', label='copy')

plt.xscale('log') # , base=2)
plt.yscale('log')

plt.xlabel('Vector length (N)')
plt.ylabel('GFlops')
plt.title('Runtime performance vector copy')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.legend()
plt.tight_layout()
plt.show()



