import csv
import time
from selenium import webdriver

def watch_videos(video_id, video_duration):
    driver = webdriver.Chrome()
    print(video_id + " started")
    driver.get("https://www.youtube.com/shorts/" + video_id)
    time.sleep(int(video_duration))
    print(video_id + " finished")
    driver.quit()
