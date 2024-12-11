
from .nodes.LoadLoraFromCivitAI import LoadLoraFromCivitAIWithDownloader
from .nodes.LoadLoraFromHF import LoadLoraFromHFWithDownloader

NODE_CLASS_MAPPINGS = { 
    "LoadLoraFromCivitAI":LoadLoraFromCivitAIWithDownloader,
    "LoadLoraFromHF":LoadLoraFromHFWithDownloader,

}
NODE_DISPLAY_NAME_MAPPINGS = { 
    "LoadLoraFromCivitAI" : "Load Lora From CivitAI",
     "LoadLoraFromHF" : "Load Lora From HuggingFace",
}


__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']