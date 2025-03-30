# import os
# import platform
# import subprocess
# import gc
# import time
# import ctypes
# from ctypes import wintypes
# import psutil
# import sys

# class ClearRAM:
#     """
#     清理系统RAM的节点，支持Windows和Linux系统。
#     提供高级内存清理选项。
#     """
    
#     @classmethod
#     def INPUT_TYPES(cls):
#         return {
#             "required": {
#                 "trigger": ("BOOLEAN", {"default": True, "label_on": "清理", "label_off": "不清理"}),
#             },
#             "optional": {
#                 "clean_file_cache": ("BOOLEAN", {"default": True, "label": "清理文件缓存"}),
#                 "clean_processes": ("BOOLEAN", {"default": True, "label": "清理进程内存"}),
#                 "clean_swap": ("BOOLEAN", {"default": False, "label": "清理交换空间"}),
#                 "retry_times": ("INT", {"default": 1, "min": 1, "max": 5, "step": 1}),
#                 "anything": ("*", {"default": None, "forceInput": False}),
#             }
#         }
    
#     RETURN_TYPES = ("STRING", "FLOAT", "FLOAT", "*",)
#     RETURN_NAMES = ("结果", "内存使用率(%)", "可用内存(MB)", "传递值",)
#     FUNCTION = "clear_ram"
#     CATEGORY = "系统工具"
    
#     def get_ram_usage(self):
#         """获取当前内存使用情况"""
#         vm = psutil.virtual_memory()
#         return vm.percent, vm.available / (1024 * 1024)
    
#     def clear_ram(self, trigger=True, clean_file_cache=True, clean_processes=True, 
#                  clean_swap=False, retry_times=1, anything=None):
#         if not trigger:
#             current_usage, available_mb = self.get_ram_usage()
#             return ("未执行清理操作", current_usage, available_mb, anything)
        
#         system = platform.system()
#         result_message = ""
        
#         try:
#             # 获取清理前的内存使用情况
#             current_usage, available_mb = self.get_ram_usage()
#             result_message += f"开始清理RAM - 当前使用率: {current_usage:.1f}%, 可用: {available_mb:.1f}MB\n"
            
#             # 执行Python垃圾回收
#             collected = gc.collect()
#             result_message += f"Python垃圾回收完成，释放了{collected}个对象。\n"
            
#             if system == "Windows":
#                 # Windows特有的清理方法
#                 for attempt in range(retry_times):
#                     if clean_file_cache:
#                         try:
#                             ctypes.windll.kernel32.SetSystemFileCacheSize(-1, -1, 0)
#                             result_message += "文件缓存清理完成。\n"
#                         except Exception as e:
#                             result_message += f"清理文件缓存失败: {str(e)}\n"
                    
#                     if clean_processes:
#                         cleaned_processes = 0
#                         for process in psutil.process_iter(['pid', 'name']):
#                             try:
#                                 handle = ctypes.windll.kernel32.OpenProcess(
#                                     wintypes.DWORD(0x001F0FFF),
#                                     wintypes.BOOL(False),
#                                     wintypes.DWORD(process.info['pid'])
#                                 )
#                                 ctypes.windll.psapi.EmptyWorkingSet(handle)
#                                 ctypes.windll.kernel32.CloseHandle(handle)
#                                 cleaned_processes += 1
#                             except:
#                                 continue
#                         result_message += f"已清理{cleaned_processes}个进程的工作集。\n"

#                     if clean_swap:
#                         try:
#                             ctypes.windll.kernel32.SetProcessWorkingSetSize(-1, -1, -1)
#                             result_message += "虚拟内存清理完成。\n"
#                         except Exception as e:
#                             result_message += f"释放虚拟内存失败: {str(e)}\n"

#                     # 使用PowerShell额外清理
#                     try:
#                         subprocess.run(["powershell", "-Command", "& {[System.GC]::Collect(); [System.GC]::WaitForPendingFinalizers()}"], 
#                                       check=True, capture_output=True)
#                         result_message += "PowerShell内存清理完成。\n"
#                     except Exception as e:
#                         result_message += f"PowerShell内存清理失败: {str(e)}\n"
                    
#                     if attempt < retry_times - 1:
#                         time.sleep(1)  # 在重试之间等待
            
#             elif system == "Linux":
#                 # Linux清理方法 - 优化版
#                 for attempt in range(retry_times):
#                     # 同步文件系统缓冲区到磁盘
#                     os.system("sync")
#                     result_message += "文件系统同步完成。\n"
                    
#                     if clean_file_cache:
#                         # 清理页面缓存、目录项和inode缓存
#                         try:
#                             # 尝试不同的方法清理缓存
#                             cache_cleared = False
                            
#                             # 方法1: 使用sudo直接写入
#                             try:
#                                 subprocess.run(["sudo", "sh", "-c", "echo 3 > /proc/sys/vm/drop_caches"], 
#                                               check=True, capture_output=True, timeout=5)
#                                 result_message += "页面缓存、目录项和inode缓存清理完成。\n"
#                                 cache_cleared = True
#                             except:
#                                 pass
                                
#                             # 方法2: 尝试直接写入
#                             if not cache_cleared:
#                                 try:
#                                     with open("/proc/sys/vm/drop_caches", "w") as f:
#                                         f.write("3")
#                                     result_message += "页面缓存、目录项和inode缓存清理完成。\n"
#                                     cache_cleared = True
#                                 except:
#                                     pass
                            
#                             # 方法3: 使用sysctl命令
#                             if not cache_cleared:
#                                 try:
#                                     subprocess.run(["sudo", "sysctl", "vm.drop_caches=3"], 
#                                                   check=True, capture_output=True, timeout=5)
#                                     result_message += "页面缓存、目录项和inode缓存清理完成。\n"
#                                     cache_cleared = True
#                                 except:
#                                     pass
                            
#                             if not cache_cleared:
#                                 result_message += "文件缓存清理失败：需要root权限。\n"
                                
#                         except Exception as e:
#                             result_message += f"文件缓存清理出错: {str(e)}\n"
                    
#                     if clean_processes:
#                         # 清理进程内存 - Linux版本
#                         cleaned_processes = 0
#                         current_pid = os.getpid()
                        
#                         # 遍历进程并尝试清理
#                         for proc in psutil.process_iter(['pid', 'name']):
#                             try:
#                                 pid = proc.info['pid']
                                
#                                 # 跳过当前进程和系统关键进程
#                                 if pid == current_pid or pid < 1000:
#                                     continue
                                
#                                 # 获取进程内存信息
#                                 process = psutil.Process(pid)
                                
#                                 # 尝试使用POSIX madvise等效功能
#                                 # 注意：这里我们只能通过发送SIGUSR1信号来建议进程释放内存
#                                 # 实际效果取决于进程是否处理了这个信号
#                                 try:
#                                     # 只对内存使用较多的进程发送信号
#                                     if process.memory_info().rss > 100 * 1024 * 1024:  # 大于100MB
#                                         os.kill(pid, 10)  # SIGUSR1
#                                         cleaned_processes += 1
#                                 except:
#                                     pass
#                             except:
#                                 continue
                        
#                         # 强制执行系统内存回收
#                         try:
#                             # 调整内核参数以更积极地回收内存
#                             subprocess.run(["sudo", "sh", "-c", "echo 1 > /proc/sys/vm/compact_memory"], 
#                                           check=False, capture_output=True)
#                         except:
#                             pass
                        
#                         result_message += f"已尝试清理{cleaned_processes}个进程的内存。\n"
                    
#                     if clean_swap:
#                         # 清理交换空间
#                         try:
#                             # 获取当前交换空间使用情况
#                             swap_before = psutil.swap_memory()
                            
#                             if swap_before.used > 0:
#                                 # 尝试使用swapoff和swapon重置交换空间
#                                 try:
#                                     # 这需要root权限
#                                     subprocess.run(["sudo", "swapoff", "-a"], check=False, capture_output=True)
#                                     time.sleep(1)
#                                     subprocess.run(["sudo", "swapon", "-a"], check=False, capture_output=True)
                                    
#                                     # 检查交换空间是否减少
#                                     swap_after = psutil.swap_memory()
#                                     freed_swap = (swap_before.used - swap_after.used) / (1024 * 1024)
                                    
#                                     if freed_swap > 0:
#                                         result_message += f"交换空间清理完成，释放了{freed_swap:.1f}MB。\n"
#                                     else:
#                                         result_message += "交换空间已清理，但使用量未减少。\n"
#                                 except:
#                                     result_message += "交换空间清理失败：需要root权限。\n"
#                             else:
#                                 result_message += "交换空间未使用，无需清理。\n"
#                         except Exception as e:
#                             result_message += f"交换空间清理出错: {str(e)}\n"
                    
#                     # 尝试使用系统调用直接释放内存
#                     try:
#                         # 使用malloc_trim释放glibc堆内存
#                         if hasattr(ctypes.CDLL('libc.so.6'), 'malloc_trim'):
#                             ctypes.CDLL('libc.so.6').malloc_trim(0)
#                             result_message += "系统堆内存整理完成。\n"
#                     except:
#                         pass
                    
#                     if attempt < retry_times - 1:
#                         time.sleep(1)  # 在重试之间等待
            
#             else:
#                 result_message += f"不支持的操作系统: {system}\n"
            
#             # 获取清理后的内存使用情况
#             time.sleep(1)  # 等待系统更新内存状态
#             current_usage, available_mb = self.get_ram_usage()
#             result_message += f"清理完成 - 最终内存使用率: {current_usage:.1f}%, 可用: {available_mb:.1f}MB"
            
#         except Exception as e:
#             result_message += f"RAM清理过程出错: {str(e)}"
#             current_usage, available_mb = self.get_ram_usage()
        
#         return (result_message, current_usage, available_mb, anything)

# NODE_CLASS_MAPPINGS = {
#     "ClearRAM": ClearRAM
# }

# NODE_DISPLAY_NAME_MAPPINGS = {
#     "ClearRAM": "清理系统内存"
# }
