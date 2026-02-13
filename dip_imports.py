import math
import sys
from cv2 import imread, imwrite, imshow
from cv2 import namedWindow, waitKey, putText
from cv2 import LINE_AA, FONT_HERSHEY_SIMPLEX
import numpy
from matplotlib.pylab import zeros
from argparse import ArgumentParser
from enum import Enum
import os
from pathlib import Path