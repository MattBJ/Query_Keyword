import os

directory = "/home/"
custom_dir = raw_input("Enter custom directory to search\ndefault is: %s\n" % directory)
if(custom_dir):
	directory = custom_dir
print(directory)

keyword = raw_input("Keyword: ")

extension_list = []
header_extension = "h"
c_file_extension = "c"
#extension_list.append(header_extension,c_file_extension)
#cpp_flag = raw_input("include cpp files?")
#print(cpp_flag)
#if(ord(cpp_flag.lower()) is ord('y')):
cpp_file_extension = "cpp"
	#print(cpp_file_extension)
	#extension_list.append(cpp_file_extension)

py_file_extension = "py"



# Here we're getting the full path string for all files we are going to search

query_file_paths = [] # if I ever want to grab the file name: query_file_paths[n].split('/')[-1] --> Parses the path by directories and grabs the last item

for dirName, subdirList, fileList in os.walk(directory):
	#print('In directory: %s' % dirName)
	# filter the fileList
	# query_file_list = list(set(query_files) & set(fileList))
	# Goes through every file name
	for fname in fileList:
		#print('\t%s' % fname)
		cmp_file = fname.split('.')[-1]
		#print("compare file %s" % cmp_file)
		#print("cmp_file (%s) is cpp_file_extension (%s): %r" %(cmp_file, cpp_file_extension, cmp_file == cpp_file_extension))
		if(cmp_file == header_extension or cmp_file == c_file_extension or cmp_file == cpp_file_extension or cmp_file == py_file_extension):
			#print("FOUND A FUCKIN FILE")
			query_file_paths.append(dirName + '/' + fname)

# print("\n\n\n\n")
# print(query_file_paths)
#print(len(query_file_paths))

# Now we have all of the paths for every file we are going to search our keyword for

# Next piece is to take the keyword from the user from earlier and find all instances of the word in the files!!!

# To do this, need to open all files in the query_file_paths list, read in each line and convert to lower (ADD AN OPTION FOR THE USER TO MATCH CASE LATER)


keyword_fileDict = {} # stores the path as the key and line/column pairs as the value list
file_iter = 0 # this is to keep track of the actual iteration of files, which will be used for query_files list
for filename in query_file_paths:
	# print("Filename to open: %s" % filename)
	if(os.access(filename, os.R_OK)): # have read access
		with open(filename) as f:
			lines = f.readlines() # now we have a list element of every line

			# for now will just get the line number, later might add the column
			instance_list = []
			line_count = 1 # gedit starts at line 1
			for line in lines:
				# goes through each line
				if(keyword.lower() in line.lower()):
					# found an instance, may be multiple in the line
					# note: find returns (-1) if did not find the substring
					col = line.lower().find(keyword.lower()) + 1
					while(col): # gedit starts all arrays at 1
						coordinate_list = [line_count,col]
						# print(coordinate_list)
						instance_list.append(coordinate_list)
						col = line.lower().find(keyword.lower(),col) + 1 # find(..., col) means now we start searching after we found the last instance in the line
				line_count += 1
			if(instance_list): # if we found any instances
				#print("instance list: ", instance_list)
				keyword_fileDict[filename] = instance_list
			# So now we can find the keyword in each line, find out what line number it's at and what element
			# this was just for debugging, looking at a file
			#for line in lines:
			#	print(line)
			#raw_input("Just control-C this bitch")

# Theoretically (testing needed), should have a dictionary of all paths and instances to keyword spots

print(keyword_fileDict)

print("Below is a list of all files and instances of the keyword available in your directory:")
start_flag = False
# Need to run a one line command for gedit
gedit_str_prefix = "gedit " # then need to add the path, and the line number
bash_command_list = []
for key in keyword_fileDict:
	print(key.split('/')[-1])
	first_line_flag = False
	for value in keyword_fileDict[key]:
		print("\tline: %d \tcolumn: %d" % (value[0], value[1]))
		if(not first_line_flag):
			line = value[0]		
			first_line_flag = True
	# Now we can open gedit using the OS!
	if(not start_flag):
		option = '-s'
		#option = ''		
		start_flag = True
	else:
		option = ''
	fname = str(key)
	line = '+' + str(line)
	#gedit_str += fname + ' '# + line + ' '
	bash_command_list.append(gedit_str_prefix + option + ' ' + fname + ' ' + line + ' &\n')

bash_file = "open_source_code.sh"

F = open(bash_file,'w')

for source in bash_command_list:
	F.write(source)

F.close()

os.system('sh ' + bash_file)

# generate bash script using what we get from the files and lines

# os.system(gedit_str)


#gedit_str = "gedit " + str(keyword_fileDict.keys()[0])

#os.system(gedit_str)

# Final notes for now: If I were to add any more functionality it would be to find:
	# Function definitions
	# Typedef definitions
	# Struct initializations







