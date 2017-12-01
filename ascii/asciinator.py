#!/usr/bin/env python
import sys
if len(sys.argv) != 4:
    print( 'Usage: ./asciinator.py image scale factor' )
    sys.exit()

from PIL import Image
import numpy as np

#chars = np.asarray(list('@&B9#SGHMh352AXsri;:,. '))
chars = np.asarray(list('@#Xr:. '))
N = len(chars)
f, W, H = sys.argv[1], int(sys.argv[2]), int(int(sys.argv[3])*(5.0/7))
# TODO it seems i have broken my ascii program . pls check up on it
img = np.asarray( Image.open(f).resize((W,H)) ).mean(2)
#get image, resize to WxH, average out (aka grayscale)
img-=img.min() #make the minimum 0
img *= (float(N-1)/img.max()) #Shift values to make max N
img = chars[img.astype(int)] #translate into ascii
print( "\n".join( ("".join(r) for r in img ) ) )