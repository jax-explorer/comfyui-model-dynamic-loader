import hashlib
import os

import folder_paths

class ComfyOnlineSaveFile:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "file_path": ("STRING", {"tooltip": "filename"})
            },
        }

    CATEGORY = "comfyonline-dynamic"
    OUTPUT_NODE = True


    RETURN_TYPES = ()
    FUNCTION = "save"

    def save(self, file_path):
        file_path = os.path.abspath(file_path)
        output_dir = folder_paths.get_output_directory()
        output_dir = os.path.abspath(output_dir)
        print(f"file_path is {file_path}, output_dir is {output_dir}")
        # 判断路径是否在输出目录中
        if file_path.startswith(output_dir):
            # 仅返回文件名
            filename = os.path.basename(file_path)
        else:
            filename = None  # 如果不在目录中，返回 None 或者提示无效路径
            
        results = list()
        results.append({
                "filename": filename,
                "subfolder": "",
                "type": "output"
        })
        return { "ui": { "file": results } }