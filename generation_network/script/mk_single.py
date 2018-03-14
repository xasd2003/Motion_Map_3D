import feature
import sys, os
import numpy as np

from PIL import Image

if __name__ == '__main__':

	if( len( sys.argv ) != 4 ):
		print 'Usage : python <progname> <img_dir> <output_dir> <split_file>'
		exit()

	progname, img_dir, output_dir, split_file = sys.argv
	
	i = 0
	
	train_set = set()

	if split_file :
		train_set = set([x.strip().split()[0].split('/')[1] for x in open(split_file).readlines()])

	

	for root, dirs, files in os.walk(img_dir):
		if root.split('.')[-1][:3] == 'avi' and '_sp_' in root:
			name = root.split('/')[-1]
			video_name = name.split('.')[0] + '.avi'
			if video_name not in train_set: continue
			if '_crop_4_mr_0' not in name: continue
			print i
			i = i + 1
			sp_id = int(root.split('/')[-1].split('_')[-1])
			out_dir = root.replace(img_dir, output_dir)
			out_dir = out_dir.replace('_sp_%s' % sp_id, '')
			out_dir = out_dir + '_L_16'
			if not os.path.exists(out_dir):
				os.system('mkdir %s -p' % (out_dir))

			if not os.path.exists('%s' % (out_dir + os.sep + '%06d' % (sp_id + 1) + '.jpg')):
				#in_dir = root.replace(img_dir,'./data/UCF101_256_crop_224_sp_16/')
				#in_dir = in_dir.replace('_L_16','')
				#ll = len([x for x in os.listdir(root)])
				#dyimg = feature.get_dynamic_image_of_video(root + os.sep,1,ll)
				#xmax, xmin = np.max(dyimg), np.min(dyimg)
				#ymax = 255
				#dyimg = (dyimg - xmin) / (xmax - xmin)
				#dyimg *= ymax
				#img = Image.fromarray( np.uint8(dyimg) )
				#img.save("%s" % ( out_dir + os.sep + '%06d' % (sp_id + 1) + '.jpg' ) )
				print 'cp %s %s' % ( root + os.sep + '000001.jpg', out_dir + os.sep + '%06d' % (sp_id + 1) + '.jpg')
				os.system('cp %s %s' % ( root + os.sep + '000001.jpg', out_dir + os.sep + '%06d' % (sp_id + 1) + '.jpg'))
