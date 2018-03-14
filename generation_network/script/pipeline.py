import os, sys
import shelve
from ywnlib.io import feature_to_image

def ucf101_get_label(name):
	cls = name.split('_')[1]
	return cls_label[cls]

def get_label(name):
	if dataset == 'UCF101':
		return ucf101_get_label(name)

def init_label(cls_label_file):
	cls_label = {}
	for line in open(cls_label_file):
		label, cls = line.split()
		label = int(label) - 1
		cls_label[cls] = label
	return cls_label

if __name__ == '__main__':
	if len(sys.argv) != 9:
		print 'Usage : python <progname> <dataset> <image_dir> <cls_label_file> <new_run_flag> <base_model> <batch_size> <L> <split_file>'
		exit()
	
	progname, dataset, image_dir, cls_label_file, new_run_flag, base_model, batch_size, L, split_file = sys.argv

	new_run_flag = int(new_run_flag)
	batch_size = int(batch_size)
	L = int(L)
	if split_file == '0':
		split_file = None
	
	# load data info
	print 'loading data info'

	train_set = set()

	if split_file:
		train_set = set([x.strip().split()[0].split('/')[1] for x in open(split_file).readlines()])

	if new_run_flag:
		print 'New Run : prepare data'
		cnt = 0

		cls_label = init_label(cls_label_file)
		data_info = {}

		for root, dirs, files in os.walk(image_dir):
			if root.split('.')[-1][:3] == 'avi':
				name = root.split('/')[-1]
				video_name = name.split('.')[0] + '.avi'
				if split_file and video_name not in train_set: continue
				label = get_label(video_name)
				max_id = len(files)
				data_info[name] = (label, max_id)
				cnt += 1
				if cnt % 1000 == 0:
					print 'cnt = %d' % cnt
		sv = shelve.open('./data/shelve/data_info')
		sv['cls_label'] = cls_label
		sv['data_info'] = data_info
		sv.close()
	else:
		print 'Load shelve'
		sv = shelve.open('./data/shelve/data_info')
		cls_label = sv['cls_label']
		data_info = sv['data_info']
		sv.close()
	
	input_dir = './data/input/'
	output_dir = './data/output/'

	dir_list = []

	#########################
	#Init
	#########################

	if os.path.exists(input_dir):
		os.system('rm -rf %s' % (input_dir))
	
	os.system('mkdir %s' % (input_dir))
	list_file = open('./config/list_file', 'w')
	output_file = open('./config/output_file', 'w')

	output_size = 0

	print 'Image data init'

	for name in data_info:
		label, max_id = data_info[name]
		for fid in range(1, max_id - L + 1, L / 2):
			inst_dir = input_dir + os.sep + name + '_L_%d_fid_%d' % (L, fid) + os.sep
			out_dir = output_dir + os.sep + name + '_L_%d_fid_%d' % (L, fid) + os.sep
			im_dir = image_dir + os.sep + name + os.sep
			list_file.write('%s %d %d\n' % (inst_dir, 1, label))
			output_file.write('%s\n' % (out_dir + '%06d' % (1)))
			output_size += 1
			os.system('mkdir %s' % (inst_dir))
			os.system('ln -s %s %s' %(im_dir + os.sep + '%06d' % (fid) + '.jpg', inst_dir + os.sep + '%06d' % (1) + '.jpg'))
			os.system('ln -s %s %s' %(im_dir + os.sep + '%06d' % (fid + 1) + '.jpg', inst_dir + os.sep + '%06d' % (2) + '.jpg'))
	list_file.close()
	output_file.close()

	os.system('cp ./config/list_file ./config/list_file_allbackup')
	
	for step in range(L - 2):
		print 'step : %d / %d' % (step + 1, L - 2)
		if os.path.exists(output_dir):
			os.system('rm -rf %s' % (output_dir))
		os.system('mkdir %s' % (output_dir))

		for name in data_info:
			label, max_id = data_info[name]
			for fid in range(1, max_id - L + 1, L / 2):
				out_dir = output_dir + os.sep + name + '_L_%d_fid_%d' % (L, fid) + os.sep
				os.system('mkdir %s' % (out_dir))

		# MARK

		fo = open('./config/output_file', 'r')
		fl = open('./config/list_file_allbackup', 'r')

		buffer_size = 100000

		while True:
			ft = open('./config/tmp', 'w')
			cnt = 0
			for line in fo:
				ft.write(line)
				cnt += 1
				if cnt == buffer_size: break
			ft.close()

			ft = open('./config/list_file', 'w')
			cnt = 0
			for line in fl:
				ft.write(line)
				cnt += 1
				if cnt == buffer_size: break
			ft.close()

			if cnt == 0 : break

			os.system('GLOG_logtostderr=1 ./tools/C3D-master/build/tools/extract_image_features.bin ./script/fmn_deploy %s 0 %d %d ./config/tmp conv2a' % (base_model, batch_size, (cnt - 1) / batch_size + 1))

			ft = open('./config/tmp', 'r')
			for line in ft:
				all_name = line.split('/')[4]
				name = line.split('/')[4].split('_L_')[0]
				fid = int(all_name.split('_')[-1])
				inst_dir = input_dir + os.sep + all_name + os.sep
				out_dir = output_dir + os.sep + all_name + os.sep
				im_dir = image_dir + os.sep + name + os.sep
				os.system('rm -f %s/*.jpg' % (inst_dir))
				feature_to_image.feature_to_image(out_dir + os.sep + '%06d' % (1) + '.conv2a', inst_dir + os.sep + '%06d' % (1) + '.jpg')
				os.system('rm -f %s' % (out_dir + os.sep + '%06d' % (1) + '.conv2a'))
				os.system('ln -s %s %s' %(im_dir + os.sep + '%06d' % (fid + step + 2) + '.jpg', inst_dir + os.sep + '%06d' % (2) + '.jpg'))

			if cnt < buffer_size : break
		fo.close()
		fl.close()
