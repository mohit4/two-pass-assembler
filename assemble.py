#code for one pass assembler
import json
import re

inset = None
memory = {}	#2011 : "3f"
labels = {}	#pas : 2010

#to be called only after one pass
def two_pass():
	global memory, labels
	for i in range(2000,2000+len(memory.keys())):
		if memory[i] in labels.keys():
			addr = labels[memory[i]]
			memory[i] = addr%100
			memory[i+1] = (addr-addr%100)/100
	print "labels",labels
	for i in memory:
		print i, memory[i]

#to perform one pass and add items to memory
#and add labels
def one_pass(lines):
	global labels, memory
	#assuming the origin of code at 2000
	counter = 2000
	#start iterating on lines
	for line in lines:
		tokens = re.split(' |,',line)
		ln = len(tokens)
		tokens = [x.lower() for x in tokens]
		print tokens
		if ln==3:
			if tokens[0][-1]=='i':
				memory[counter]=inset[tokens[0]][tokens[1]]
				counter=counter+1
				memory[counter]=tokens[2]
			else:
				memory[counter]=inset[tokens[0]][tokens[1]][tokens[2]]
			counter=counter+1
		elif ln==2:
			#check for labels here
			if tokens[0][0]=='j':
				memory[counter]=inset[tokens[0]]
				counter=counter+1
				#if label exist in labels
				if tokens[1] in labels.keys():
					memory[counter]=labels[tokens[1]]%100
					counter=counter+1
					memory[counter]=(labels[tokens[1]]-labels[tokens[1]]%100)/100
					counter=counter+1
				else:
					memory[counter]=tokens[1]
					counter=counter+1
					memory[counter]=tokens[1]
					counter=counter+1
					labels[tokens[1]]=None
			else:	
				memory[counter]=inset[tokens[0]][tokens[1]]
				counter=counter+1
		elif ln==1:
			#check for lable
			#definition of a label
			if tokens[0][-1]==':':
				labels[tokens[0][0:-1]]=counter
			else:
				memory[counter]=inset[tokens[0]]
				counter=counter+1
	two_pass()

#to load the file for reading
def load_file(fileName):
	asCode = open(fileName,'r')
	text = asCode.read()
	asCode.close()
	lines = [x for x in re.split('\n',text) if len(x)>0]
	one_pass(lines)

#to load the instruction set
def load_inset():
	global inset
	with open('inset.json') as json_file:
		inset = json.load(json_file)

def main():
	fileName='newfile.asm'
	load_inset()
	load_file(fileName)

if __name__ == '__main__':
	main()