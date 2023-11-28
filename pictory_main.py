import time

import chatGpt
import pictory_selenium
from pictory_selenium import Pictory
import ChatGptYouTubeMetaData
import get_videoFile_path
import template_ids


def pictory_automation(topic_name):
    title, content = chatGpt.getChatGptResponse(topic_name)
    time.sleep(60)  # Waiting a min to avoid RPM clash
    youtube_meta_data = ChatGptYouTubeMetaData.getYoutubeMetaData(content)
    print("Obtained youtube_meta_data :", youtube_meta_data)
    template_style = youtube_meta_data['category']
    template_list = [x for x in template_ids.template_name.keys()]
    if template_style not in template_list:
        print("template_style :", template_style, "given in meta-data is not in the pictory template list. So select "
                                                  "some default template to proceed.")
        template_style = 'Subtitle Default'
    try:
        pictory_obj = Pictory(topic_tile=title,
                              topic_content=content,
                              template_style=template_style,
                              voice_accent='Aditi',
                              voice_speed_percentage='100',
                              background_music='off',
                              aspect_ratio='16_9',
                              download_path='D:\\PictoryDownloads',
                              logo_path='D:\\PictoryTopicsList\\logo.png'
                              )

        pictory_obj.open_pictory_browser()

        pictory_obj.pictory_editor_page()

        pictory_obj.choose_template()

        pictory_obj.customize_video()

        pictory_obj.prepare_video_download()

        pictory_obj.final_video_download()

        file_path = get_videoFile_path.get_most_recent_file("D:\\PictoryDownloads")

        pictory_obj.youtube_upload(file_path=file_path,
                                   title=youtube_meta_data['title'],
                                   description=youtube_meta_data['description'],
                                   keywords=youtube_meta_data['tags'],
                                   privacy_status="public"
                                   )

        pictory_obj.close_browser()

        return True

    except Exception as exp:
        print("Exception occurred in pictory_main.py - pictory_automation", exp)
