import time
from qango6x6 import Quango6x6
from bitops import bitops
import numpy as np
import util
import random
import sys

b = bitops()
q = Quango6x6()

pos = [
    int("0b110010001001010001100110001010110100",2),
    int("0b001101010010101100010001110100001011",2)
]

trueset = set()
falseset = set()
booldict = {}
numvals = 100000
for a in range(numvals):
    if random.random()>0.5:
        trueset.add(a)
        booldict[a]=True
    else:
        falseset.add(a)
        booldict[a]=False

checker = np.random.randint(0,int(numvals*1.5),100)

start = time.perf_counter()

tflist = []
for check in checker:
    if check in trueset:
        tflist.append(True)
    elif check in falseset:
        tflist.append(False)
    else:
        tflist.append(None)

end = time.perf_counter()
print(end-start)
print(sys.getsizeof(trueset) + sys.getsizeof(falseset))


start = time.perf_counter()

tflist = []
for check in checker:
    if check in booldict:
        tflist.append(booldict[check])
    else:
        tflist.append(None)

end = time.perf_counter()
print(end-start)
print(sys.getsizeof(booldict))
