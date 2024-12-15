
from .nodes.LoadLoraFromCivitAI import LoadLoraFromCivitAIWithDownloader
from .nodes.LoadLoraFromHF import LoadLoraFromHFWithDownloader
from .nodes.LoadHunyuanLoraFromCivitAI import LoadHunyuanLoraFromCivitAIWithDownloader
from .nodes.upload_anything import UploadAnything
from .nodes.save_file import ComfyOnlineSaveFile

NODE_CLASS_MAPPINGS = { 
    "LoadLoraFromCivitAI":LoadLoraFromCivitAIWithDownloader,
    "LoadHunyuanLoraFromCivitAI":LoadHunyuanLoraFromCivitAIWithDownloader,
    "LoadLoraFromHF":LoadLoraFromHFWithDownloader,
    "ComfyOnlineUploadAnything": UploadAnything,
    "ComfyOnlineSaveFile": ComfyOnlineSaveFile

}
NODE_DISPLAY_NAME_MAPPINGS = { 
    "LoadLoraFromCivitAI" : "Load Lora From CivitAI",
    "LoadLoraFromHF" : "Load Lora From HuggingFace",
    "LoadHunyuanLoraFromCivitAI": "Load HunyuanLora From CivitAI",
    'ComfyOnlineUploadAnything': "ComfyOnlineUploadAnything",
    "ComfyOnlineSaveFile": "ComfyOnlineSaveFile"
}

WEB_DIRECTORY = "./web"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', "WEB_DIRECTORY"]