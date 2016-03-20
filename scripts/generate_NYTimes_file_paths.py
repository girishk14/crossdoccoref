import os
import sys


file_list = []
root_path =  '/home/network/girishk14/crossdoccoref/data/NYTimes/Text'


for root, _, filenames in os.walk(root_path):	
	for filename in filenames:
        	 file_list.append(os.path.join(root, filename))

for x in file_list:
     print x
