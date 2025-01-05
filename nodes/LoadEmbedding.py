
import folder_paths

class EmbeddingLoader:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": { 
                "embedding_name": (folder_paths.get_filename_list("embeddings"), {"tooltip": "The name of the embeddings."}),
                "strength_embedding": ("FLOAT", {"default": 1.0, "min": -100.0, "max": 100.0, "step": 0.01, "tooltip": "How strongly to modify the diffusion model. This value can be negative."}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    FUNCTION = "load_embedding"

    CATEGORY = "embeddings"
    DESCRIPTION = "embedding loader"

    def load_embedding(self, embedding_name, strength_embedding):
        if strength_embedding == 0:
            return ("", )

        embedding_text = f"(embedding:{embedding_name}:{strength_embedding})"
        return (embedding_text, )