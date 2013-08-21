import json
import numpy as np
import sys
import difflib
import csv
from pprint import pprint
from collections import OrderedDict
from collections import defaultdict

data = [3.5,2.0]
#weights = [1./20,1./5]
a = 20
b = 5
axis = 0
#weighted_average = np.average(data,axis,weights)
weighted_average = np.average(data,0,[1./a,1./b])

print weighted_average
