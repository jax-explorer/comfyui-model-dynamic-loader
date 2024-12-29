
from .nodes.LoadLoraFromCivitAI import LoadLoraFromCivitAIWithDownloader
from .nodes.LoadLoraFromHF import LoadLoraFromHFWithDownloader
from .nodes.LoadLoraFromComfyOnline import LoadLoraFromComfyOnlineWithDownloader
from .nodes.nodes import LoadHunyuanLoraFromCivitAIWithDownloader
from .nodes.nodes import LoadHunyuanLoraFromHFWithDownloader
from .nodes.nodes import LoadHunyuanLoraFromComfyOnlineWithDownloader
from .nodes.upload_anything import UploadAnything
from .nodes.save_file import ComfyOnlineSaveFile

NODE_CLASS_MAPPINGS = { 
    "LoadLoraFromCivitAI":LoadLoraFromCivitAIWithDownloader,
    "LoadLoraFromComfyOnline":LoadLoraFromComfyOnlineWithDownloader,
    "LoadHunyuanLoraFromCivitAI":LoadHunyuanLoraFromCivitAIWithDownloader,
    "LoadHunyuanLoraFromComfyOnline":LoadHunyuanLoraFromComfyOnlineWithDownloader,
    "LoadHunyuanLoraFromHF":LoadHunyuanLoraFromHFWithDownloader,
    "LoadLoraFromHF":LoadLoraFromHFWithDownloader,
    "ComfyOnlineUploadAnything": UploadAnything,
    "ComfyOnlineSaveFile": ComfyOnlineSaveFile

}
NODE_DISPLAY_NAME_MAPPINGS = { 
    "LoadLoraFromCivitAI" : "Load Lora From CivitAI",
    "LoadLoraFromComfyOnline": "Load Lora From ComfyOnline",
    "LoadLoraFromHF" : "Load Lora From HuggingFace",
    "LoadHunyuanLoraFromComfyOnline":" Load Lora From ComfyOnline",
    "LoadHunyuanLoraFromCivitAI": "Load HunyuanLora From CivitAI",
    "LoadHunyuanLoraFromHF": "Load HunyuanLora From HF",
    'ComfyOnlineUploadAnything': "ComfyOnlineUploadAnything",
    "ComfyOnlineSaveFile": "ComfyOnlineSaveFile"
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', "WEB_DIRECTORY"]