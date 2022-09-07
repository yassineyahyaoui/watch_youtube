import os
import csv
from functions.get_videos import get_videos
from functions.watch_videos import watch_videos


def main():
    #get_videos("FOOT BALL", "UCJvgF5uUL22U7i9tNlPvduA", True)
    with open(os.path.join("data", "FOOT BALL", "videos.csv"), "r") as videos_file:
        content = csv.DictReader(videos_file)
        for i in range(10):
            for video in content:
                print(video["Video id"], video["Video duration"][2:-1])
                watch_videos(video["Video id"], video["Video duration"][2:-1])


if __name__ == "__main__":
    main()
