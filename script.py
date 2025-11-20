import os
import shutil

if os.path.exists("Day3.txt"):
    os.makedirs("Completed", exist_ok=True)
    shutil.move("Day3.txt", "Completed")
    print("File moved successfully!")
else:
    print("Target file doesn't exist!")
