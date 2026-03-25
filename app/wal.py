class WAL:
    def __init__(self, filepath):
        self.filepath = filepath
        self.sequence_no = 1
    
    def append(self, record:str):
        with open(self.filepath, "a") as f:
            f.write(str(self.sequence_no) + "|" + record + "\n")
            self.sequence_no += 1
