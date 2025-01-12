import os
import sys
import torch
import numpy as np
from torch.utils.data import Dataset
import skvideo.io as skv


class Atari(Dataset):
    def __init__(self, root, mode, gamelist=None):
        assert mode in ['train', 'validation', 'test'], f'Invalid dataset mode "{mode}"'

        # self.video_path = os.checkpointdir.join(root, f'{key_word}')
        self.video_path = root
        self.video_fn = [os.path.join(fn, mode, img) for fn in os.listdir(root)
                         if gamelist is None or fn in gamelist
                         for img in os.listdir(os.path.join(root, fn, mode))]
        self.video_fn.sort()


    def __getitem__(self, index):
        fn = self.video_fn[index]
        video = skv.vread(os.path.join(self.video_path, fn), outputdict={
            "-sws_flags": "bilinear",
            "-s": "128x128"
        })
        # pil_img = Image.open(os.path.join(self.video_path, fn)).convert('RGB')
        # pil_img = pil_img.resize((128, 128), PIL.Image.BILINEAR)

        video_arr = torch.from_numpy(video / 255).permute(0, 3, 1, 2)
        video_t = video_arr[::2].float()
        # print(video_t.shape) = torch.Size([10, 3, 128, 128])
        return video_t

    def __len__(self):
        return len(self.video_fn)
