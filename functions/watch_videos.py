import csv
from selenium import webdriver

def watch_videos(video_id):
    driver = webdriver.Chrome()
    driver.get("https://www.youtube.com/shorts/" + video_id)
