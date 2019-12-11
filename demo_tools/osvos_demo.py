from __future__ import print_function

"""
Sergi Caelles (scaelles@vision.ee.ethz.ch)

This file is part of the OSVOS paper presented in:
    Sergi Caelles, Kevis-Kokitsi Maninis, Jordi Pont-Tuset, Laura Leal-Taixe, Daniel Cremers, Luc Van Gool
    One-Shot Video Object Segmentation
    CVPR 2017
Please consider citing the paper if you use this code.
"""
import os
import sys
from PIL import Image
import imageio
import numpy as np
import tensorflow as tf

slim = tf.contrib.slim

# Import OSVOS files
root_folder = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(root_folder))
from osvos_net.net import OSVOS
from data_utils.dataset import Dataset

osvos = OSVOS()
# User defined parameters
gpu_id = 0

# Train parameters
parent_path = os.path.join('models', 'OSVOS_parent', 'OSVOS_parent.ckpt-50000')

max_training_iters = 500

# Show results
overlay_color = [255, 0, 0]
transparency = 0.5


def demo(seq_name, learning_rate=1e-8,
         save_step=max_training_iters,
         side_supervision=3, display_step=10, train_model=True):
    result_path = os.path.join('tmp', seq_name, 'pred')
    concate_path = os.path.join('tmp', seq_name, 'concat')

    logs_path = os.path.join('models', seq_name)

    # Define Dataset
    test_frames = sorted(
        os.listdir(os.path.join('tmp', seq_name, 'img')))
    test_imgs = [os.path.join('tmp', seq_name, 'img', frame) for
                 frame in test_frames]

    if not os.path.exists(concate_path):
        os.makedirs(concate_path)
    if not os.path.exists(result_path):
        os.makedirs(result_path)
    if train_model:
        train_imgs = [os.path.join('tmp', seq_name, 'img', '00000.jpg') + ' ' +
                      os.path.join('tmp', seq_name, 'first_mask.png')]
        dataset = Dataset(train_imgs, test_imgs, './', data_aug=True)
    else:
        dataset = Dataset(None, test_imgs, './')

    # Train the network
    if train_model:
        with tf.Graph().as_default():
            with tf.device('/gpu:' + str(gpu_id)):
                global_step = tf.Variable(0, name='global_step',
                                          trainable=False)
                osvos.train_finetune(dataset, parent_path, side_supervision,
                                     learning_rate, logs_path,
                                     max_training_iters,
                                     save_step, display_step, global_step,
                                     iter_mean_grad=1, ckpt_name=seq_name)

    # Test the network
    with tf.Graph().as_default():
        with tf.device('/gpu:' + str(gpu_id)):
            checkpoint_path = tf.train.latest_checkpoint(
                os.path.join('models', seq_name))
            osvos.test(dataset, checkpoint_path, result_path)

    for img_p in test_frames:
        frame_num = img_p.split('.')[0]
        img = np.array(Image.open(
            os.path.join('tmp', seq_name, "img", img_p)))
        mask = np.array(
            Image.open(os.path.join(result_path, frame_num + '.jpg')))
        mask = mask // np.max(mask)
        im_over = np.ndarray(img.shape, dtype=np.float)
        im_over[:, :, 0] = (1 - mask) * img[:, :, 0] + mask * (
                overlay_color[0] * transparency + (1 - transparency) * img[:, :,
                                                                       0])
        im_over[:, :, 1] = (1 - mask) * img[:, :, 1] + mask * (
                overlay_color[1] * transparency + (1 - transparency) * img[:, :,
                                                                       1])
        im_over[:, :, 2] = (1 - mask) * img[:, :, 2] + mask * (
                overlay_color[2] * transparency + (1 - transparency) * img[:, :,
                                                                       2])
        im_over = np.where(im_over > 255, 255, im_over)
        im_over = im_over.astype(np.uint8)
        imageio.imwrite(os.path.join(concate_path, frame_num + ".jpg"), im_over)


# For test
if __name__ == '__main__':
    seq_name = "car-shadow"
    demo(seq_name, train_model=True)
