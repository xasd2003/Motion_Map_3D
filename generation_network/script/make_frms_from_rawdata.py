import os, sys, cv2, math

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print 'Usage python <progname> <input_dir> <output_dir>'
		exit()
	input_dir = sys.argv[1]
	output_dir = sys.argv[2]
	info_cnt = 0
	info_mis = 0
	for root, dirs, files in os.walk(input_dir):
		for _file in files:
			t_file = root + os.sep + _file
			new_file = root + os.sep + _file.replace('(', '').replace(')', '')
			if t_file != new_file:
				os.rename(t_file, new_file)
				t_file = new_file
				_file = _file.replace('(', '').replace(')', '')
			t_dir = root.replace(input_dir, output_dir + os.sep) + os.sep + _file + os.sep
			videoCapture = cv2.VideoCapture(t_file)
			if not videoCapture : continue
			count = int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
			flag = videoCapture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, count)
			total_time = videoCapture.get(cv2.cv.CV_CAP_PROP_POS_MSEC) / 1000
			if (total_time < 1e-4):
				continue
			fps = count / total_time
			if not (fps and count):
				continue
			if fps < 0 or count < 0:
				continue
			if 1.0 * count / fps > 10000000:
				continue
			print (_file, fps, count, total_time)
			os.system('mkdir -p %s' % t_dir)
			p = int(fps) / 2
			cnt = 1
			while cnt <= 16:
				p = int(fps) / 2
				while True:
					flag = videoCapture.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, p)
					if not flag:
						break
					flag, frame = videoCapture.read()
					if not flag:
						break
					frame = cv2.resize(frame, (112, 112))
					cv2.imwrite(t_dir + os.sep + '%06d.jpg' % cnt, frame)
					cnt += 1
					p += fps / 4
					p = math.ceil(p)
					if p > count : break
			info_cnt += 1
			if cnt < 17:
				info_mis += 1
			print info_mis, info_cnt

	print info_mis, info_cnt
