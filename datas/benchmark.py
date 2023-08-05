import os
import glob
import random
import pickle

import numpy as np
import imageio
import torch
import torch.utils.data as data
import skimage.color as sc
from torch.utils.data import DataLoader
import time
from utils import ndarray2tensor


class Benchmark(data.Dataset):
    def __init__(self, HR_folder, LR_folder, scale=2, colors=1):
        super(Benchmark, self).__init__()
        self.HR_folder = HR_folder
        self.LR_folder = LR_folder

        self.img_postfix = '.png'
        self.scale = scale
        self.colors = colors

        self.nums_dataset = 0

        self.hr_filenames = glob.glob(self.HR_folder + '\\*.png')
        self.hr_filenames.sort()
        self.lr_filenames = glob.glob(self.LR_folder + '\\*.png')
        self.lr_filenames.sort()
        # self.hr_filenames = []
        # self.lr_filenames = []
        ## generate dataset
        tags = os.listdir(self.HR_folder)
        # for tag in tags:
        #     hr_filename = os.path.join(self.HR_folder, tag)
        #     lr_filename = os.path.join(self.LR_folder, 'X{}'.format(scale), tag.replace('.png', 'x{}.png'.format(self.scale)))
        #     self.hr_filenames.append(hr_filename)
        #     self.lr_filenames.append(lr_filename)
        self.nums_trainset = len(self.hr_filenames)
        ## if store in ram
        self.hr_images = []
        self.lr_images = []

        LEN = len(self.hr_filenames)
        for i in range(LEN):
            lr_image, hr_image = imageio.imread(self.lr_filenames[i], pilmode="RGB"), imageio.imread(self.hr_filenames[i], pilmode="RGB")
            if self.colors == 1:
                lr_image, hr_image = sc.rgb2ycbcr(lr_image)[:, :, 0:1], sc.rgb2ycbcr(hr_image)[:, :, 0:1]
            self.hr_images.append(hr_image)
            self.lr_images.append(lr_image) 

    def __len__(self):
        return len(self.hr_filenames)
    
    def __getitem__(self, idx):
        # get whole image, store in ram by default
        lr, hr = self.lr_images[idx], self.hr_images[idx]
        lr_h, lr_w, _ = lr.shape
        hr = hr[0:lr_h*self.scale, 0:lr_w*self.scale, :]
        lr, hr = ndarray2tensor(lr), ndarray2tensor(hr)
        return lr, hr
