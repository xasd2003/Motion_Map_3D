import os, sys
import random

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'Usage : python <progname> <input_file> <output_file>'
		exit()
	progname, input_file, output_file = sys.argv
	lines = open(input_file).readlines()
	random.shuffle(lines)
	open(output_file, 'w').write(''.join(lines))
