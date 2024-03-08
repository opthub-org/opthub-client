import os

class MatchSelectionContext:
    def __init__(self):
        self.file_path = ".match_selection"
        self.competition_id = None
        self.match_id = None
        self.load()
    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r') as file:
                    content = file.read()
                    parts = content.split(",")
                    self.competition_id = parts[0]
                    if len(parts) > 1:
                        self.match_id = parts[1]
                    else:
                        print("tmp file does not found.")
            except IOError as e:
                # file read error
                print(f"An error occurred while reading the file: {e}")
        else:
            # file not found
            print("No .match_selection file found. Using default values.")
        pass
    def update(self,competition_id, match_id):
        self.competition_id = competition_id
        self.match_id = match_id
        with open(self.file_path, 'w') as file:
            file.write(competition_id + "," + match_id)
        pass