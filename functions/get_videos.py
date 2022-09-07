import os
import csv
import pandas
import googleapiclient.discovery
import googleapiclient.errors


api_service_name = "youtube"
api_version = "v3"
developer_key = "AIzaSyCQ7pxDuHY2_bymJf0ZbqUFXIFQ36TLYdo"


def get_videos(targeted_channel, channel_id, shorts):
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)
    request = youtube.search().list(
        part="snippet,id",
        channelId=channel_id,
        order="date",
        maxResults=50
    )
    response = request.execute()

    if not os.path.exists(os.path.join("data", targeted_channel, "videos.csv")):
        os.mkdir("data")
        os.mkdir("data/" + targeted_channel)
        file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "w", newline="")
        file_videos.close()

    file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "r", newline="")
    content = file_videos.read()
    file_videos.close()

    if ("Channel name" or "Video id" or "Video title" or "Video publish time") not in content:
        file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "w", newline="")
        row = ("Channel name", "Video id", "Video title", "Video publish time")
        csv.writer(file_videos).writerow(row)
        file_videos.close()

    for video in response["items"]:
        if "videoId" in video["id"]:
            file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "r", newline="")
            content = file_videos.read()
            file_videos.close()

            if video["id"]["videoId"] not in content:
                file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "a", newline="")

                channel_title = video["snippet"]["channelTitle"].encode("utf-8")
                video_id = video["id"]["videoId"]
                video_title = video["snippet"]["title"].encode("utf-8")
                video_publish_time = video["snippet"]["publishTime"]

                row = (channel_title, video_id, video_title, video_publish_time)
                csv.writer(file_videos).writerow(row)
                file_videos.close()

    get_videos_details(targeted_channel, shorts)
    sort_videos_by_rating(targeted_channel)


def get_videos_details(targeted_channel, shorts):
    videos_list = []
    file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "r", newline="")
    content = csv.DictReader(file_videos)
    for row in content:
        videos_list.append(row)
    file_videos.close()

    file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "w", newline="")
    row = ("Channel name", "Video id", "Video title", "Video description", "Video thumbnail", "Video category", "Video rating", "Video view count",
           "Video like count", "Video comment count", "Video license", "Video duration", "Video publish time")
    csv.writer(file_videos).writerow(row)

    for video in videos_list:
        youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=developer_key)
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video["Video id"]
        )
        response = request.execute()

        if response["items"]:
            channel_name = response["items"][0]["snippet"]["channelTitle"].encode("utf-8")
            video_id = response["items"][0]["id"]
            video_title = response["items"][0]["snippet"]["title"].encode("utf-8")
            video_description = response["items"][0]["snippet"]["description"].encode("utf-8")
            video_thumbnail = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]
            video_category = response["items"][0]["snippet"]["categoryId"]
            video_view_count = response["items"][0]["statistics"]["viewCount"]
            if "likeCount" in response["items"][0]["statistics"]:
                video_like_count = response["items"][0]["statistics"]["likeCount"]
            else:
                video_like_count = "0"
            if "commentCount" in response["items"][0]["statistics"]:
                video_comment_count = response["items"][0]["statistics"]["commentCount"]
            else:
                video_comment_count = "0"

            if int(video_view_count) != 0:
                video_rating = ((int(video_like_count) + (int(video_comment_count) * 10)) / int(video_view_count)) * 100
            else:
                video_rating = 0

            video_license = response["items"][0]["contentDetails"]["licensedContent"]
            video_duration = response["items"][0]["contentDetails"]["duration"]
            video_publish_time = response["items"][0]["snippet"]["publishedAt"]

            if not video_license and (video_duration.find("M") == -1 or not shorts):
                row = (channel_name, video_id, video_title, video_description, video_thumbnail, video_category, video_rating, video_view_count, video_like_count,
                       video_comment_count, video_license, video_duration, video_publish_time)
                csv.writer(file_videos).writerow(row)

    file_videos.close()


def sort_videos_by_rating(targeted_channel):
    data = pandas.read_csv(os.path.join("data", targeted_channel, "videos.csv"))
    data.sort_values(["Video rating"], axis=0, ascending=[False], inplace=True)

    videos_list = []
    file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "r", newline="")
    content = csv.DictReader(file_videos)
    for row in content:
        videos_list.append(row)
    file_videos.close()

    file_videos = open(os.path.join("data", targeted_channel, "videos.csv"), "w", newline="")
    row = ("Channel name", "Video id", "Video title", "Video description", "Video thumbnail", "Video category", "Video rating", "Video view count",
           "Video like count", "Video comment count", "Video license", "Video duration", "Video publish time")
    csv.writer(file_videos).writerow(row)
    for index, item in data.iterrows():
        for video in videos_list:
            if item["Video id"] == video["Video id"]:
                row = (video["Channel name"], video["Video id"], video["Video title"], video["Video description"], video["Video thumbnail"], video["Video category"], video["Video rating"], video["Video view count"], video["Video like count"], video["Video comment count"], video["Video license"], video["Video duration"], video["Video publish time"])
                csv.writer(file_videos).writerow(row)
    file_videos.close()
