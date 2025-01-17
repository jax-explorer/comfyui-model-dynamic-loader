import os
import folder_paths
import re
import json
import io
    
class TextSave:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""

    @classmethod
    def INPUT_TYPES(s):
        return {"required": { "text": ("STRING", )},
                }

    RETURN_TYPES = ()
    FUNCTION = "save_text"

    OUTPUT_NODE = True

    CATEGORY = "text"

    def save_text(self, text,):
        filename_prefix = "ComfyUI_Text"
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        results = list()
        file = f"{filename_prefix}_{counter:05}_.txt"
        with open(os.path.join(full_output_folder, file), 'w') as f:
            f.write(text)
        results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
        })

        return { "ui": { "text": results } }