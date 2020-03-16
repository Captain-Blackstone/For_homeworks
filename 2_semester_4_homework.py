import os
import shutil
import pathlib
import glob

# Create a folder

if not os.path.exists("I_was_made_by_os/"):
    os.mkdir("I_was_made_by_os/")
folder = pathlib.Path("I_was_made_by_pathlib/")
folder.mkdir(exist_ok=True)

# Move a file into it

shutil.move("ftps", "I_was_made_by_os/") # In
shutil.move("I_was_made_by_os/ftps", "./") # Out

file = pathlib.Path("ftps")
file.replace(folder / file) # In
pathlib.Path(folder / file).replace(file) # Out

# Making additional files and moving them to the same directory
for i in range(10):
    file = "file" + str(i)
    os.mknod(file)
pattern = glob.glob("file*")
for p in pattern:
    shutil.move(p, "I_was_made_by_os/")

for i in range(10):
    file = pathlib.Path("file" + str(i))
    file.touch()
pattern = pathlib.Path("./").glob("file*")
for p in pattern:
    p.replace(folder/p)

# Renaming

shutil.move("I_was_made_by_os/file0", "I_was_made_by_os/I_was_renamed_by_shutil")

file_to_rename = pathlib.Path("I_was_made_by_pathlib/file0")
file_to_rename.rename(file_to_rename.with_name("I_was_renamed_by_pathlib"))

# Listing directories
for file in os.listdir("I_was_made_by_os"):
    print(file)
print("----")
for file in os.scandir("I_was_made_by_os"):
    print(file)
print("----")
for file in folder.glob("*"):
    print(file.stem)

# Deleting
shutil.rmtree("I_was_made_by_os/")

for file in folder.glob("*"):
    file.unlink()
folder.rmdir()