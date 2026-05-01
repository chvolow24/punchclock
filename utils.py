def load_file_string(filepath):
    filestr = ""
    with open(filepath, "r") as f:
        filestr = f.read()
    return filestr
