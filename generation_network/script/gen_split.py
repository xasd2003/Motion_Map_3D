import sys, os
import shelve
from ywnlib.io import feature_to_image

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'Usage : python <progname> <input_dir> <output_dir>'
		exit()

	progname, input_dir, output_dir = sys.argv
	cnt = 0
	for root, dirs, files in os.walk(input_dir):
		if root.split('.')[-1][:3] == 'avi':
			name = root.split('/')[-1]
			max_id = len(files)
			img_num = max_id / 16
			more_id = max_id % 16
			for i in range(max_id):
				sp_id = i / (img_num + 1)
				if sp_id < more_id:
					img_id = i % (img_num + 1)
				else:
					sp_id = more_id + (i - more_id*(img_num+1))/img_num
					img_id = (i - more_id*(img_num+1)) % img_num
				out_dir = output_dir + os.sep + name + '_sp_%d' % (sp_id) + os.sep
				if not os.path.exists(out_dir):
					os.system('mkdir %s -p' % (out_dir))
				#print root + os.sep + '%06d' % (i + 1) + '.jpg'
				if not os.path.exists(out_dir + os.sep + '%06d' % (img_id + 1) + '.jpg'):
					os.system('ln -s %s %s' % (root + os.sep + '%06d' % (i + 1) + '.jpg', out_dir + os.sep + '%06d' % (img_id + 1) + '.jpg'))
				if cnt % 1000 == 0:
					print "cnt = %s" % cnt
				cnt += 1
	
	print cnt
