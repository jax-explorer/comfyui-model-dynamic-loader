#import install
from .cai_utils import download_cai

import comfy.sd
import comfy.utils

import folder_paths
import os
import requests
import torch
import numpy as np
from PIL import Image, ImageOps, ImageSequence
from io import BytesIO
import tempfile

class LoadImageFromURL:
    @classmethod
    def INPUT_TYPES(s):
        return {"required":
                    {"url": ("STRING", {"default": ""})},
                }

    CATEGORY = "image"

    RETURN_TYPES = ("IMAGE", "MASK")
    FUNCTION = "load_image"
    
    def pillow(self, func, *args, **kwargs):
        """Helper function to handle PIL operations safely"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"PIL operation failed: {e}")
            raise e
    
    def load_image(self, url):
        try:
            # Download image from URL
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Load image from response content
            img = self.pillow(Image.open, BytesIO(response.content))
            
            output_images = []
            output_masks = []
            w, h = None, None

            excluded_formats = ['MPO']
            
            for i in ImageSequence.Iterator(img):
                i = self.pillow(ImageOps.exif_transpose, i)

                if i.mode == 'I':
                    i = i.point(lambda i: i * (1 / 255))
                image = i.convert("RGB")

                if len(output_images) == 0:
                    w = image.size[0]
                    h = image.size[1]
                
                if image.size[0] != w or image.size[1] != h:
                    continue
                
                image = np.array(image).astype(np.float32) / 255.0
                image = torch.from_numpy(image)[None,]
                if 'A' in i.getbands():
                    mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                    mask = 1. - torch.from_numpy(mask)
                else:
                    mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
                output_images.append(image)
                output_masks.append(mask.unsqueeze(0))

            if len(output_images) > 1 and img.format not in excluded_formats:
                output_image = torch.cat(output_images, dim=0)
                output_mask = torch.cat(output_masks, dim=0)
            else:
                output_image = output_images[0]
                output_mask = output_masks[0]

            return (output_image, output_mask)
        except Exception as e:
            print(f"Error loading image from URL: {e}")
            # Return a small blank image and mask in case of error
            blank_image = torch.zeros((1, 64, 64, 3), dtype=torch.float32, device="cpu")
            blank_mask = torch.zeros((1, 64, 64), dtype=torch.float32, device="cpu")
            return (blank_image, blank_mask)