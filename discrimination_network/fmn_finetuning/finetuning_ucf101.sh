mkdir -p LOG_TRAIN

GLOG_log_dir="./LOG_TRAIN" ./tools/C3D-v1.1/build/tools/caffe.bin train --solver=./script/fmn_finetuning/solver_r2.prototxt --weights=./model/c3d_resnet18_sports1m_r2_iter_2800000.caffemodel --gpu=0
