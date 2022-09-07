import os
import csv
from functions.get_videos import get_videos
from functions.watch_videos import watch_videos


def main():
    #get_videos("FOOT BALL", "UCJvgF5uUL22U7i9tNlPvduA", True)
    with open(os.path.join("data", "FOOT BALL", "videos.csv"), "r") as videos_file:
        content = csv.DictReader(videos_file)
        for video in content:
            print(video["Video id"], video["Video duration"][2:-1])

    # watch_videos("3Mby-4JpdY0")


if __name__ == "__main__":
    main()
