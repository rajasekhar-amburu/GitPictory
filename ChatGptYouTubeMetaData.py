from openai import OpenAI, OpenAIError
import config
import json
from retry import retry

client = OpenAI(api_key=config.chat_gpt_secret_key)


@retry(tries=3, delay=60, backoff=30, max_delay=30, jitter=(1, 2), logger=None)
def getYoutubeMetaData(request_data=None):
    try:
        print("Querying Chat-GPT to get the meta data from the response we got in the prev request")
        query = ("Hey ChatGPT, Please read the below content which i am going to use for youtube. "
                 "I want you to help me to give a proper title, description and tags. Give at-least 15 tags"
                 "Also choose one category of the content from the below list1 only"
                 "list1 = ['Marketing', 'Business', 'Real Estate', 'Professional', 'Rouge', 'Sunrise', 'Wellness', 'Science', 'Executive', 'Caption Grey', 'Black and White', 'Remote', 'Lemon', 'Facts and Figures', 'Metro', 'Metro Caption', 'Investigate', 'Samaritan', 'Books', 'Luxurious', 'Home', 'Graceful', 'Unity', 'Strategy', 'Epicure', 'Saturate', 'SketchMark', 'Florentine', 'Money', 'Slate', 'Print', 'Flashlight', 'Beach', 'Land', 'Earth', 'Natural', 'Retro Boutique', 'Beauty', 'Tracer', 'Fun', 'Cosmic', 'Synth', 'Subtitle Standard', 'Technology', 'Party', 'Fashion', 'Bricks', 'Moonrise', 'Letter', 'Elegant', 'Standard', 'Caption Dark', 'Caption Highlight', 'Caption Italics', 'Caption Thin', 'Caption Yellow', 'Caption Fade', 'Caption Subtitles', 'Travel', 'Pictory', 'Subtitle Default']"
                 "Category value should be one in the list1 only. Please give the response in json format like this "
                 "{'title': '<title-comes-here>', 'description':'<description-comes-here>', 'tags':'tag1, tag2, tag3, tag4, tag5, tag-n'}, 'category': '<one-of-the-list1-item>'"
                 "\n\n" + request_data)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": query}
            ]
        )
        json_response = response.model_dump_json()
        response_dict = json.loads(json_response)
        gpt_response = response_dict['choices'][0]['message']['content']
        meta_data = eval(gpt_response)
        return meta_data
    except OpenAIError as exp:
        print("OpenAIError occurred: ", exp)
        raise  # Re-raise the exception after logging
    except Exception as exp:
        print("Exception occurred at ChatGptYouTubeMetaData.py : ", exp)
        raise
