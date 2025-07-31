import sublime
import sublime_plugin
import subprocess
import os
import re

class TerminalSwitcherCommand(sublime_plugin.WindowCommand):
    def run(self):
        # 弹出一个简单的选择菜单
        self.window.show_quick_panel(
            ["PowerShell", "Kali Linux (WSL)", "Ubuntu (WSL)"],
            self.on_done
        )
    
    def on_done(self, index):
        # 获取当前文件所在的目录，如果没有打开文件，则默认使用用户的工作目录
        active_view = self.window.active_view()
        if active_view and active_view.file_name():
            file_path = active_view.file_name()
            dir_path = os.path.dirname(file_path)
        else:
            dir_path = os.getcwd()  # 如果没有打开文件，则使用当前工作目录
        
        # 根据选择的索引执行相应的命令
        if index == 0:
            self.open_powershell(dir_path)
        elif index == 1:
            self.open_kali_linux(dir_path)
        elif index == 2:
            self.open_ubuntu(dir_path)
    
    def get_current_dir(self):
        """获取当前文件所在目录"""
        active_view = self.window.active_view()
        if active_view and active_view.file_name():
            file_path = active_view.file_name()
            return os.path.dirname(file_path)
        else:
            return os.getcwd()
    
    def windows_path_to_wsl_path(self, windows_path):
        """将Windows路径转换为WSL路径"""
        # 标准化路径分隔符
        windows_path = windows_path.replace('\\', '/')
        
        # 转换驱动器路径 (例如: C:/Users -> /mnt/c/Users)
        if re.match(r'^[A-Za-z]:', windows_path):
            drive_letter = windows_path[0].lower()
            path_without_drive = windows_path[2:] if len(windows_path) > 2 else ''
            return '/mnt/{}{}'.format(drive_letter, path_without_drive)
        
        return windows_path
    
    def open_powershell(self, dir_path):
        """使用指定路径启动 PowerShell"""
        try:
            # 按优先级尝试不同的PowerShell命令
            powershell_commands = [
                "pwsh",           # PowerShell 7+ (通过PATH)
                "powershell"      # Windows PowerShell 5.1 (通过PATH)
            ]
            
            success = False
            for ps_cmd in powershell_commands:
                try:
                    subprocess.Popen([
                        ps_cmd, 
                        "-NoExit", 
                        "-Command", 
                        "Set-Location -Path '{}'".format(dir_path)
                    ])
                    success = True
                    break
                except (FileNotFoundError, OSError):
                    continue
            
            if not success:
                sublime.error_message("未找到PowerShell，请确保PowerShell已安装并在系统PATH中")
                
        except Exception as e:
            sublime.error_message("启动PowerShell时发生错误: {}".format(str(e)))
    
    def open_kali_linux(self, dir_path):
        """使用 WSL 启动 Kali Linux 并指定目录"""
        try:
            wsl_path = self.windows_path_to_wsl_path(dir_path)
            
            # 使用Windows Terminal启动WSL (如果可用)
            try:
                subprocess.Popen([
                    "wt", 
                    "wsl", 
                    "-d", "kali-linux", 
                    "--cd", wsl_path
                ])
            except FileNotFoundError:
                # 如果Windows Terminal不可用，使用传统方法
                subprocess.Popen([
                    "wsl", 
                    "-d", "kali-linux", 
                    "--exec", "bash", 
                    "-c", "cd '{}' && exec bash".format(wsl_path)
                ], creationflags=subprocess.CREATE_NEW_CONSOLE)
                
        except Exception as e:
            sublime.error_message("启动Kali Linux时发生错误: {}".format(str(e)))
    
    def open_ubuntu(self, dir_path):
        """使用 WSL 启动 Ubuntu 并指定目录"""
        try:
            wsl_path = self.windows_path_to_wsl_path(dir_path)
            
            # 使用Windows Terminal启动WSL (如果可用)
            try:
                subprocess.Popen([
                    "wt", 
                    "wsl", 
                    "-d", "Ubuntu", 
                    "--cd", wsl_path
                ])
            except FileNotFoundError:
                # 如果Windows Terminal不可用，使用传统方法
                subprocess.Popen([
                    "wsl", 
                    "-d", "Ubuntu", 
                    "--exec", "bash", 
                    "-c", "cd '{}' && exec bash".format(wsl_path)
                ], creationflags=subprocess.CREATE_NEW_CONSOLE)
                
        except Exception as e:
            sublime.error_message("启动Ubuntu时发生错误: {}".format(str(e)))


# 单独的PowerShell命令
class OpenPowershellCommand(sublime_plugin.WindowCommand):
    def run(self):
        switcher = TerminalSwitcherCommand(self.window)
        dir_path = switcher.get_current_dir()
        switcher.open_powershell(dir_path)


# 单独的Kali Linux命令
class OpenKaliLinuxCommand(sublime_plugin.WindowCommand):
    def run(self):
        switcher = TerminalSwitcherCommand(self.window)
        dir_path = switcher.get_current_dir()
        switcher.open_kali_linux(dir_path)


# 单独的Ubuntu命令
class OpenUbuntuCommand(sublime_plugin.WindowCommand):
    def run(self):
        switcher = TerminalSwitcherCommand(self.window)
        dir_path = switcher.get_current_dir()
        switcher.open_ubuntu(dir_path)

# 注册键盘快捷键
def plugin_loaded():
    pass