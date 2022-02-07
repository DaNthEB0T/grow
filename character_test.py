import os

characters = 0
lines = 0
for root, subFolders, files in os.walk("."):
    for file in files:
        if file.endswith(".py") or file.endswith(".js") or file.endswith(".html") or file.endswith(".css") or file.endswith(".txt"):
            fullpath = os.path.join(root, file)
            with open(fullpath, "r") as f:
                characters += len(f.read())
            with open(fullpath, "r") as f:
                lines += sum(1 for line in f.readlines())
            
print(f"Lines: {lines}\nCharacters: {characters}")