#import install
from .cai_utils import download_cai


import comfy.sd
import comfy.utils

import folder_paths
import os

class LoadCheckpointFromCivitAIWithDownloader:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "civitai_model_id": ("STRING", {"default": "", "tooltip": "The ID of the model to download from CivitAI."}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP", "VAE")
    FUNCTION = "load_and_download_checkpoint"
    CATEGORY = "checkpoint"

    def load_and_download_checkpoint(self, civitai_model_id):
        # 获取 CivitAI Token
        civitai_token_id = os.getenv("CIVITAI_TOKEN", "").strip()
        if not civitai_token_id:
            raise RuntimeError("CIVITAI_TOKEN environment variable is not set or empty.")
        # 目标存储路径为 loras 目录
        checkpoint_dir = folder_paths.get_folder_paths("checkpoints")[0]

        # 下载文件到 loras 目录
        checkpoint_filename = f"tmp_{civitai_model_id or 'downloaded_checkpoint'}.safetensors"  # 生成临时文件名
        checkpoint_path = os.path.join(checkpoint_dir, checkpoint_filename)
        
        self.download_from_civitai(civitai_model_id, civitai_token_id, checkpoint_path)

        out = comfy.sd.load_checkpoint_guess_config(checkpoint_path, output_vae=True, output_clip=True, embedding_directory=folder_paths.get_folder_paths("embeddings"))

        # 加载后删除临时文件
        try:
            os.remove(checkpoint_path)
        except Exception as e:
            print(f"Failed to delete temporary checkpoint file: {e}")

        return out[:3]

    def download_from_civitai(self, model_id, token_id, lora_path):
        print("Downloading checkpoint from CivitAI")
        print(f"\tModel ID: {model_id}")
        print(f"\tToken ID: {token_id}")
        print(f"\tSave path: {lora_path}")
        # 实现下载逻辑
        download_cai(model_id, token_id, lora_path)