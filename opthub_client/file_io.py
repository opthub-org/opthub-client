import os

class FileHandler:
    def __init__(self):
        self.file_path = "./file_handler_config.txt"

    def read(self):
        # ファイルが存在するかチェック
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                return file.read()
        else:
            # ファイルが存在しない場合、空の文字列を返す
            return ""

    def write(self, data):
        with open(self.file_path, 'w') as config_file:
            config_file.write(data)
