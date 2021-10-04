## Checks if annotations files describes boxes smaller than 16px when resized

from os import path, chdir, getcwd, listdir
from sys import argv

DIRS = ["train", "validation", "test"]


if len(argv) < 2:
    print("Write training width or height, example: 416 or 512 or 608, etc")
    raise SystemExit

try:
    size = int(argv[1])
    if (size % 32) != 0:
        print("Your width/height is not perfect divisible by 32")
        raise SystemExit
    if size < 32:
        print("Your width/height is not positive or perfect divisible by 32")
        raise SystemExit
except (TypeError, ValueError):
    print("Write training width or height, must be a positive integer")
    raise SystemExit

chdir(path.join("OIDv6", "multidata"))

for DIR in DIRS:
    chdir(DIR)
    for filename in listdir(getcwd()):
        if path.isfile(filename) and filename.endswith(".jpg"):
            labels_file = path.join(getcwd(), filename[:-4] + ".txt")
            labels = [line.strip() for line in open(labels_file, "r")]
            for idx, label in enumerate(labels):
                try:
                    _, _, _, relative_width, relative_height = label.split()
                    box_scaled_width = float(relative_width) * size
                    if box_scaled_width < 16:
                        print(f"{DIR}/{filename} box #{idx+1} will have a width of {box_scaled_width}")
                        continue
                    box_scaled_height = float(relative_height) * size
                    if box_scaled_height < 16:
                        print(f"{DIR}/{filename} box #{idx+1} will have a height of {box_scaled_height}")
                        continue
                except ValueError:
                    print(f"{DIR}/{filename} box #{idx+1} is invalid")
    chdir("..")
