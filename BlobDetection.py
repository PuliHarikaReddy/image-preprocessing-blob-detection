import cv2
import sys
import scipy.ndimage as ndi
import scipy
import numpy as np
import math
from math import pi
import PIL
from PIL import Image
import scipy.misc
import imageio
import random


src1 = sys.argv[1]
img = Image.open(src1).convert('L')
print("Grayscale Image Saved")  
imageio.imwrite('grayscale.png', img)                                   
img_array = np.array(img, dtype = float)                                 

thresholdValue = int(input("Enter Threshold Value:"))	
maximumValue = 255
im_bin = (img_array < thresholdValue) * maximumValue
imageio.imwrite('binary.png', im_bin)
print("Binary Image Saved")  

print ("starting first pass")
curr_label = 1;
img_array = im_bin
labels = im_bin

label_conv = []
label_conv.append([])
label_conv.append([])

count = 0
for i in range(1, len(img_array)):
	for j in range(1, len(img_array[0])):

		if img_array[i][j] > 0:
			label_x = labels[i][j - 1]
			label_y = labels[i - 1][j]

			if label_x > 0:
		
				if label_y > 0:

					if not label_x == label_y:
						labels[i][j] = min(label_x, label_y)
						if max(label_x, label_y) not in label_conv[0]:
							label_conv[0].append(max(label_x, label_y))
							label_conv[1].append(min(label_x, label_y))
						elif max(label_x, label_y) in label_conv[0]:
							ind = label_conv[0].index(max(label_x, label_y))
							if label_conv[1][ind] > min(label_x, label_y):
								l = label_conv[1][ind]
								label_conv[1][ind] = min(label_x, label_y)
								while l in label_conv[0] and count < 100:
									count += 1
									ind = label_conv[0].index(l)
									l = label_conv[1][ind]
									label_conv[1][ind] = min(label_x, label_y)

								label_conv[0].append(l)
								label_conv[1].append(min(label_x, label_y))

					else:
						labels[i][j] = label_y
			
				else:
					labels[i][j] = label_x

		
			elif label_y > 0:
				labels[i][j] = label_y

		
			else:
				labels[i][j] = curr_label
				curr_label += 1


print ("starting second pass")
count = 1
for idx, val in enumerate(label_conv[0]):

	if label_conv[1][idx] in label_conv[0] and count < 100:
		count += 1
		ind = label_conv[0].index(label_conv[1][idx])
		label_conv[1][idx] = label_conv[1][ind]

for i in range(1, len(labels)):
	for j in range(1, len(labels[0])):

		if labels[i][j] in label_conv[0]:
			ind = label_conv[0].index(labels[i][j])
			labels[i][j] = label_conv[1][ind]

height, width = labels.shape

colors = []
colors.append([])
colors.append([])
color = 1

coloured_img = Image.new("RGB", (width, height))
coloured_data = coloured_img.load()

for i in range(len(labels)):
	for j in range(len(labels[0])):
		if labels[i][j] > 0:
			if labels[i][j] not in colors[0]:
				colors[0].append(labels[i][j])
				colors[1].append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

			ind = colors[0].index(labels[i][j])
			coloured_data[j, i] = colors[1][ind]
			
imageio.imwrite('colored.png', coloured_img)
print("Coloured Image Saved")
	

