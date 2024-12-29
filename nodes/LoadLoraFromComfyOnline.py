#import install
from .comfyonline_utils import download_comfyonline


import comfy.sd
import comfy.utils

import folder_paths
import os

class LoadLoraFromComfyOnlineWithDownloader:
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
                "comfyonline_model_id": ("STRING", {"default": "", "tooltip": "The ID of the model to download from CivitAI."}),
            }
        }

    RETURN_TYPES = ("MODEL", "CLIP")
    FUNCTION = "load_and_download_lora"
    CATEGORY = "loaders"

    def load_and_download_lora(self, model, clip, strength_model, strength_clip, comfyonline_model_id):
        # # 获取 CivitAI Token
        comfyonline_token_id = ""
        # civitai_token_id = os.getenv("CIVITAI_TOKEN", "").strip()
        # if not civitai_token_id:
        #     raise RuntimeError("CIVITAI_TOKEN environment variable is not set or empty.")
        # 目标存储路径为 loras 目录
        loras_dir = folder_paths.get_folder_paths("loras")[0]

        # 下载文件到 loras 目录
        lora_filename = f"tmp_{comfyonline_model_id or 'downloaded_lora'}.safetensors"  # 生成临时文件名
        lora_path = os.path.join(loras_dir, lora_filename)
        
        self.download_from_ComfyOnline(comfyonline_model_id, comfyonline_token_id, lora_path)

        # 加载 LoRA
        loaded_model, loaded_clip = self.load_lora(model, clip, lora_path, strength_model, strength_clip)

        # 加载后删除临时文件
        try:
            os.remove(lora_path)
        except Exception as e:
            print(f"Failed to delete temporary LoRA file: {e}")

        return loaded_model, loaded_clip

    def download_from_ComfyOnline(self, model_id, token_id, lora_path):
        print("Downloading LoRA from ComfyOnline")
        print(f"\tModel ID: {model_id}")
        print(f"\tToken ID: {token_id}")
        print(f"\tSave path: {lora_path}")
        # 实现下载逻辑
        download_comfyonline(model_id, token_id, lora_path)

    def load_lora(self, model, clip, lora_path, strength_model, strength_clip):
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
    