#import install
from .cai_utils import download_cai

import requests
from requests.exceptions import HTTPError

import comfy.sd
import comfy.utils

import folder_paths
import os

class LoadHunyuanLoraFromHFWithDownloader:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "repo": ("STRING", {"default": "", "tooltip": "The Hugging Face repository name, e.g., 'user/repo'."}),
                "file_name": ("STRING", {"default": "", "tooltip": "The file name in the Hugging Face repository."}),
                "strength": ("FLOAT", {"default": 1.0, "min": -10.0, "max": 10.0, "step": 0.0001, "tooltip": "LORA strength, set to 0.0 to unmerge the LORA"}),
            },
            "optional": {
                "prev_lora":("HYVIDLORA", {"default": None, "tooltip": "For loading multiple LoRAs"}),
                "blocks":("SELECTEDBLOCKS", ),
            }
        }

    RETURN_TYPES = ("HYVIDLORA",)
    RETURN_NAMES = ("lora", )
    FUNCTION = "getlorapath"
    CATEGORY = "HunyuanVideoWrapper"
    DESCRIPTION = "Select a LoRA model from civitAI"

    def getlorapath(self, repo, file_name, strength, blocks=None, prev_lora=None, fuse_lora=False):
        # 验证参数
        if not repo or not file_name:
            raise ValueError("Both 'repo' and 'file_name' parameters are required.")
        # 目标存储路径为 loras 目录
        loras_dir = folder_paths.get_folder_paths("tmp_hunyuan_loras")[0]

        # 下载文件到 loras 目录
        lora_filename = f"tmp_hf_{repo.replace('/', '_')}_{file_name}.safetensors"  # 生成临时文件名
        lora_path = os.path.join(loras_dir, lora_filename)
        download_url = f"https://huggingface.co/{repo}/resolve/main/{file_name}"

        self.download_from_hf(download_url, lora_path)

        loras_list = []
        lora = {
            "path": lora_path,
            "strength": strength,
            "name": lora_filename,
            "fuse_lora": fuse_lora,
            "blocks": blocks
        }
        if prev_lora is not None:
            loras_list.extend(prev_lora)

        loras_list.append(lora)
        return (loras_list,)
    
    def download_from_hf(self, url, lora_path):
        """
        从 Hugging Face 下载文件到指定路径。
        """
        print(f"Downloading LoRA from Hugging Face: {url}")
        try:
            with requests.get(url, stream=True) as response:
                response.raise_for_status()
                with open(lora_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=8192):
                        file.write(chunk)
            print(f"File downloaded successfully: {lora_path}")
            return True
        except Exception as e:
            print(f"Error downloading LoRA file from Hugging Face: {e}")
            return False
