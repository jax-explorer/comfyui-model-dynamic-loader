#import install
from .cai_utils import download_cai

import requests
from requests.exceptions import HTTPError
import re

import comfy.sd
import comfy.utils

import folder_paths
import os

class LoadLoraFromHFWithDownloader:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL", {"tooltip": "The diffusion model the LoRA will be applied to."}),
                "clip": ("CLIP", {"tooltip": "The CLIP model the LoRA will be applied to."}),
                "strength_model": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                "strength_clip": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01}),
                "repo": ("STRING", {"default": "", "tooltip": "The Hugging Face repository name, e.g., 'user/repo'."}),
                "file_name": ("STRING", {"default": "", "tooltip": "The file name in the Hugging Face repository."}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "load_and_download_lora"
    CATEGORY = "loaders"

    def load_and_download_lora(self, model, clip, strength_model, strength_clip, repo, file_name):
        # 验证参数
        if not repo or not file_name:
            raise ValueError("Both 'repo' and 'file_name' parameters are required.")

        # 构建下载 URL 和临时文件路径
        download_url = f"https://huggingface.co/{repo}/resolve/main/{file_name}"
        loras_dir = folder_paths.get_folder_paths("loras")[0]
        lora_filename = f"tmp_{repo.replace('/', '_')}_{file_name}.safetensors"  # 临时文件名
        lora_path = os.path.join(loras_dir, lora_filename)
        # 下载文件
        download_success = self.download_from_hf(download_url, lora_path)
        if not download_success:
            raise RuntimeError(f"Failed to download LoRA file from Hugging Face: {download_url}")

        # 加载 LoRA 文件
        loaded_model, loaded_clip = self.load_lora(model, clip, lora_path, strength_model, strength_clip)

        # 加载后删除临时文件
        try:
            os.remove(lora_path)
        except Exception as e:
            print(f"Failed to delete temporary LoRA file: {e}")

        return loaded_model, loaded_clip

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

    def load_lora(self, model, clip, lora_path, strength_model, strength_clip):
        """
        加载指定路径的 LoRA 文件到模型和 CLIP。
        """
        if strength_model == 0 and strength_clip == 0:
            return model, clip

        lora = None
        if self.loaded_lora is not None:
            if self.loaded_lora[0] == lora_path:
                lora = self.loaded_lora[1]
            else:
                temp = self.loaded_lora
                self.loaded_lora = None
                del temp

        if lora is None:
            lora = comfy.utils.load_torch_file(lora_path, safe_load=True)
            self.loaded_lora = (lora_path, lora)

        model_lora, clip_lora = comfy.sd.load_lora_for_models(model, clip, lora, strength_model, strength_clip)
        return model_lora, clip_lora