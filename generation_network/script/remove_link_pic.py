import os,sys


if __name__ == '__main__':

	if(len(sys.argv) != 3):
		print 'Usage : python <progname> <input_dir> <output_dir>'
		exit()

	progname, input_dir, output_dir = sys.argv

	for root, dirs, files in os.walk(input_dir):
		for _dir in dirs:
			out_dir = root.replace(input_dir, output_dir)
			if not os.path.exists(out_dir + os.sep + _dir):
				os.system('mkdir %s -p' % (out_dir + os.sep + _dir))
			true_pic = 0
			for i in range(16):
				if not os.path.islink( root + os.sep + _dir + os.sep + '%06d' % (i+1) + '.jpg'):
					os.system('cp %s %s -r' % (root + os.sep + _dir + os.sep + '%06d' % (i+1) + '.jpg', out_dir + os.sep + _dir + os.sep + '%06d' % (i+1) + '.jpg'))
					true_pic = i+1
				else:
					if true_pic == 0:
						os.system('cp %s %s -r' % (root + os.sep + _dir + os.sep + '%06d' % (i+1) + '.jpg', out_dir + os.sep + _dir + os.sep + '%06d' % (i+1) + '.jpg'))
					else:
						os.system('cp %s %s -r' % (root + os.sep + _dir + os.sep + '%06d' % (true_pic) + '.jpg', out_dir + os.sep + _dir + os.sep + '%06d' % (i+1) + '.jpg'))
