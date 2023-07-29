"""
This script is a modified version of a script originally found at: https://github.com/open-mmlab/OpenPCDet.

Many thanks to the authors of OpenPCDet for their work. 
"""
import argparse
import glob
from pathlib import Path
import os 
import pickle


import mayavi.mlab as mlab
from visual_utils import visualize_utils as V

import numpy as np
import torch

from pcdet.config import cfg, cfg_from_yaml_file
from pcdet.datasets import DatasetTemplate
from pcdet.models import build_network, load_data_to_gpu
from pcdet.utils import common_utils

def parse_config():
    parser = argparse.ArgumentParser(description='arg parser')
    parser.add_argument('--cfg_file', type=str, default='cfgs/kitti_models/pointpillar_kitti.yaml',
                        help='specify the config for demo')
    parser.add_argument('--data_path', type=str, default='/home/auzun/Documents/OpenPCDet/data/KITTI_testset/training/velodyne',
                        help='specify the point cloud data file or directory')
    parser.add_argument('--ckpt', type=str, default='/home/auzun/Documents/OpenPCDet/output/kitti_models/pointpillar_kitti/kitti_fix_seed/ckpt/checkpoint_epoch_80.pth', help='specify the pretrained model')
    parser.add_argument('--ext', type=str, default='.npy', help='specify the extension of your point cloud data file')
    parser.add_argument('--idx', type=int, default=80, help='specify the index')
    parser.add_argument('--name', type=str, default='screenshots', help='specify the name')
    args = parser.parse_args()
    cfg_from_yaml_file(args.cfg_file, cfg)
    return args, cfg



def lidar_to_rect(pts_lidar,V2C_array,R0_array):
    """
    :param pts_lidar: (N, 3)
    :return pts_rect: (N, 3)
    """
    pts_lidar_hom = cart_to_hom(pts_lidar)
    pts_rect = np.dot(pts_lidar_hom, np.dot(V2C_array.T, R0_array.T))
    # pts_rect = reduce(np.dot, (pts_lidar_hom, self.V2C.T, self.R0.T))
    return pts_rect

def cart_to_hom(pts):
    """
    :param pts: (N, 3 or 2)
    :return pts_hom: (N, 4 or 3)
    """
    pts_hom = np.hstack((pts, np.ones((pts.shape[0], 1), dtype=np.float32)))
    return pts_hom

def get_fov_flag(pts_rect, img_shape, P2_array):
    """
    Args:
        pts_rect:
        img_shape:
        calib:

    Returns:

    """
    pts_img, pts_rect_depth = rect_to_img(pts_rect, P2_array)
    val_flag_1 = np.logical_and(pts_img[:, 0] >= 0, pts_img[:, 0] < img_shape[1])
    val_flag_2 = np.logical_and(pts_img[:, 1] >= 0, pts_img[:, 1] < img_shape[0])
    val_flag_merge = np.logical_and(val_flag_1, val_flag_2)
    pts_valid_flag = np.logical_and(val_flag_merge, pts_rect_depth >= 0)

    return pts_valid_flag

def rect_to_img(pts_rect, P2_array):
    """
    :param pts_rect: (N, 3)
    :return pts_img: (N, 2)
    """
    pts_rect_hom = cart_to_hom(pts_rect)
    pts_2d_hom = np.dot(pts_rect_hom, P2_array.T)
    pts_img = (pts_2d_hom[:, 0:2].T / pts_rect_hom[:, 2]).T  # (N, 2)
    pts_rect_depth = pts_2d_hom[:, 2] - P2_array.T[3, 2]  # depth in rect camera coord
    return pts_img, pts_rect_depth


class DemoDataset(DatasetTemplate):
    def __init__(self, dataset_cfg, class_names, training=True, root_path=None, logger=None, ext='.bin'):
        """
        Args:
            root_path:
            dataset_cfg:
            class_names:
            training:
            logger:
        """
        super().__init__(
            dataset_cfg=dataset_cfg, class_names=class_names, training=training, root_path=root_path, logger=logger
        )
        self.root_path = root_path
        self.ext = ext
        data_file_list = glob.glob(str(root_path / f'*{self.ext}')) if self.root_path.is_dir() else [self.root_path]

        data_file_list.sort()
        self.sample_file_list = data_file_list

    def __len__(self):
        return len(self.sample_file_list)

    def __getitem__(self, index):
        if self.ext == '.bin':
            points = np.fromfile(self.sample_file_list[index], dtype=np.float32).reshape(-1, 4)
        elif self.ext == '.npy':
            points = np.load(self.sample_file_list[index])
        else:
            raise NotImplementedError
        P2_array = np.array([[7.21537720e+02, 0.00000000e+00, 6.09559326e+02, 4.48572807e+01],
        [0.00000000e+00, 7.21537720e+02, 1.72854004e+02, 2.16379106e-01],
        [0.00000000e+00, 0.00000000e+00, 1.00000000e+00, 2.74588400e-03]], dtype=np.float32)
        R0_array = np.array([[ 0.9999239 ,  0.00983776, -0.00744505],
        [-0.0098698 ,  0.9999421 , -0.00427846],
        [ 0.00740253,  0.00435161,  0.9999631 ]], dtype=np.float32)
        V2C_array = np.array([[ 7.53374491e-03, -9.99971390e-01, -6.16602018e-04,-4.06976603e-03],
        [ 1.48024904e-02,  7.28073297e-04, -9.99890208e-01, -7.63161778e-02],
        [ 9.99862075e-01,  7.52379000e-03,  1.48075502e-02, -2.71780610e-01]], dtype=np.float32)
        image_shape = np.array([375, 1242],dtype=np.int32)
        pts_rect = lidar_to_rect(points[:, 0:3],V2C_array,R0_array)
        fov_flag = get_fov_flag(pts_rect, image_shape, P2_array)
        points = points[fov_flag]
        input_dict = {
            'points': points,
            'frame_id': index,
        }

        data_dict = self.prepare_data(data_dict=input_dict)
        return data_dict

def main():
    args, cfg = parse_config()
    max_frame = args.idx
    save_folder_name = args.name
    logger = common_utils.create_logger()
    logger.info('-----------------Quick Demo of OpenPCDet-------------------------')
    demo_dataset = DemoDataset(
        dataset_cfg=cfg.DATA_CONFIG, class_names=cfg.CLASS_NAMES, training=False,
        root_path=Path(args.data_path), ext=args.ext, logger=logger
    )
    logger.info(f'Total number of samples: \t{len(demo_dataset)}')
    data_path = args.data_path
    pkl_path = os.path.join(os.path.dirname(os.path.dirname(data_path)), 'kitti_infos_val.pkl')

    with open(pkl_path, 'rb') as f:
        infos_val = pickle.load(f)
    

    model = build_network(model_cfg=cfg.MODEL, num_class=len(cfg.CLASS_NAMES), dataset=demo_dataset)
    model.load_params_from_file(filename=args.ckpt, logger=logger, to_cpu=True)
    model.cuda()
    model.eval()
    with torch.no_grad():
        for idx, data_dict in enumerate(demo_dataset):
            logger.info(f'Visualized sample index: \t{idx + 1}')
            data_dict = demo_dataset.collate_batch([data_dict])
            load_data_to_gpu(data_dict)
            pred_dicts, _ = model.forward(data_dict)
            file_path =demo_dataset.sample_file_list[idx] 
            file_name = os.path.basename(file_path)
            file_name_without_extension = os.path.splitext(file_name)[0]
            frame_id = int(file_name_without_extension)

            gt_boxes_lidar_variable = None  # Variable to store gt_boxes_lidar

            for info in infos_val:
                lidar_idx = int(info['point_cloud']['lidar_idx'])
                if lidar_idx == frame_id:
                    print(lidar_idx)
                    gt_boxes_lidar_variable = info['annos']['gt_boxes_lidar']


            V.draw_scenes(
                points=data_dict['points'][:, 1:], gt_boxes=gt_boxes_lidar_variable, ref_boxes=pred_dicts[0]['pred_boxes'],
                ref_scores=pred_dicts[0]['pred_scores'], ref_labels=pred_dicts[0]['pred_labels']
            )
            subfolder_path = os.path.join('./', save_folder_name)
            file_name = file_name_without_extension + '.png'
            save_name = os.path.join(subfolder_path, file_name)
            mlab.savefig(save_name)
            mlab.close()
            #mlab.show(stop=True)
            if idx == max_frame:
                break

    logger.info('Demo done.')


if __name__ == '__main__':
    main()
