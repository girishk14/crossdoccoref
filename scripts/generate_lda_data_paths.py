import os
import sys


file_list = []
root_path =  '../LDA/dataset/'


for filename in os.listdir(root_path):	
	file_list.append(os.path.join(root_path, filename))

for x in file_list:
     print x
