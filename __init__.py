
from .nodes.LoadLoraFromCivitAI import LoadLoraFromCivitAIWithDownloader
from .nodes.LoadLoraFromHF import LoadLoraFromHFWithDownloader
from .nodes.LoadHunyuanLoraFromCivitAI import LoadHunyuanLoraFromCivitAIWithDownloader

NODE_CLASS_MAPPINGS = { 
    "LoadLoraFromCivitAI":LoadLoraFromCivitAIWithDownloader,
    "LoadHunyuanLoraFromCivitAI":LoadHunyuanLoraFromCivitAIWithDownloader,
    "LoadLoraFromHF":LoadLoraFromHFWithDownloader,

}
NODE_DISPLAY_NAME_MAPPINGS = { 
    "LoadLoraFromCivitAI" : "Load Lora From CivitAI",
    "LoadLoraFromHF" : "Load Lora From HuggingFace",
    "LoadHunyuanLoraFromCivitAI": "Load HunyuanLora From CivitAI",
}


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']