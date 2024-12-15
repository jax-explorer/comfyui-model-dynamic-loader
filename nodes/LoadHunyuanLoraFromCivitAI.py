#import install
from .cai_utils import download_cai


import comfy.sd
import comfy.utils

import folder_paths
import os

class LoadHunyuanLoraFromCivitAIWithDownloader:
    def __init__(self):
        self.loaded_lora = None

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "civitai_model_id": ("STRING", {"default": "", "tooltip": "The ID of the model to download from CivitAI."}),
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

    def getlorapath(self, civitai_model_id, strength, blocks=None, prev_lora=None, fuse_lora=False):
        # 获取 CivitAI Token
        civitai_token_id = os.getenv("CIVITAI_TOKEN", "").strip()
        if not civitai_token_id:
            raise RuntimeError("CIVITAI_TOKEN environment variable is not set or empty.")
        # 目标存储路径为 loras 目录
        loras_dir = folder_paths.get_folder_paths("tmp_hunyuan_loras")[0]

        # 下载文件到 loras 目录
        lora_filename = f"tmp_civit_{civitai_model_id or 'downloaded_lora'}.safetensors"  # 生成临时文件名
        lora_path = os.path.join(loras_dir, lora_filename)
        
        self.download_from_civitai(civitai_model_id, civitai_token_id, lora_path)

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

    def download_from_civitai(self, model_id, token_id, lora_path):
        print("Downloading LoRA from CivitAI")
        print(f"\tModel ID: {model_id}")
        print(f"\tToken ID: {token_id}")
        print(f"\tSave path: {lora_path}")
        # 实现下载逻辑
        download_cai(model_id, token_id, lora_path)
