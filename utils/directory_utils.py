import os

class DirectoryUtils:
    def __init__(self):
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.parent_directory = os.path.dirname(self.current_directory)
    
    def get_path(self, *path_parts):
        """生成一个在父目录下的指定路径"""
        return os.path.join(self.parent_directory, *path_parts)
