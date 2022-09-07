import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()


def watch_videos(video_id, video_duration):
    driver.get("https://www.youtube.com/shorts/" + video_id)
    try:
        driver.find_element(By.CSS_SELECTOR, "button.ytp-large-play-button.ytp-button").click()
    except:
        pass
    time.sleep(int(video_duration) + 10)
