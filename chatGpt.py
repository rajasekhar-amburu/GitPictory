import time
from openai import OpenAI
import config
import script_content_ChatGpt
import json
from retry import retry

client = OpenAI(api_key=config.chat_gpt_secret_key)


@retry(tries=3, delay=60, backoff=30, max_delay=30, jitter=(1, 2), logger=None)
def getChatGptResponse(question=None):
    try:
        query = "within 500 words " + question + " using the below instructions \n" + script_content_ChatGpt.response_instructions + "now within 500 words " + question
        print("Quering Chat-GPT to get the response in a particular format we want.")
        time.sleep(1)
        print("Response Generation will take few min.... Please wait....")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": query}
            ]
        )
        print("We got the response from Chat-GPT.")
        json_response = response.model_dump_json()
        response_dict = json.loads(json_response)
        gpt_response = response_dict['choices'][0]['message']['content']
        print("GPT Response : ", gpt_response)
        print("Now we will prepare this response content to pass as input to the pictory.")
        return get_dict_response(gpt_response)
    except Exception as exp:
        print("Exception in chatGpt.py : getChatGptResponse() : ", exp)
        raise


response = """GPT Response :  Making money online offers countless opportunities for individuals to earn income from the comfort of their own homes. In this comprehensive guide, we will explore various methods and strategies to help you make money online.

Freelancing:
Freelancing is a versatile and lucrative option for those with marketable skills. Websites like Upwork, Freelancer, and Fiverr connect freelancers with clients seeking various services, such as graphic design, writing, programming, or virtual assistance. Start by creating a compelling profile showcasing your skills and experience. Then, bid on relevant projects and deliver high-quality work within agreed-upon deadlines to build a solid reputation and client base.

E-commerce:
Creating an online store or selling products on platforms like Amazon or eBay can be a profitable venture. Begin by identifying a niche or product that you are passionate about or have expertise in. Source or create products to sell, set up an e-commerce website, optimize it for search engines, and adopt effective marketing strategies to attract customers. Providing excellent customer service and maintaining a strong online presence are crucial for long-term success in e-commerce.

Blogging and Content Creation:
If you have a talent for writing or creating engaging content, starting a blog or YouTube channel can be a rewarding endeavor. Identify a niche that aligns with your interests or expertise, and consistently create valuable and engaging content for your audience. Monetize your blog or channel through advertisements, sponsorships, affiliate marketing, or by offering digital products such as e-books or online courses.

Online Surveys and Microtasks:
Participating in online surveys or completing microtasks can be a simple way to earn extra income. Websites like Swagbucks, InboxDollars, or Amazon Mechanical Turk offer opportunities to earn money by taking surveys, watching videos, or completing small tasks. While the income generated may not be substantial, it can provide a supplemental source of income or be a convenient way to earn money in your spare time.

Dropshipping:
Dropshipping is a business model where you sell products without having to stock inventory. You partner with a supplier who handles the storage, packaging, and shipping of the products directly to customers. Establish an online store, select products from your supplier's catalog, and market them to customers. When a customer places an order, the supplier fulfills it, and you earn a profit on the difference between the wholesale and retail prices.

Affiliate Marketing:
Affiliate marketing involves promoting other people's products or services and earning a commission for every sale made through your unique affiliate link. Join affiliate programs or networks such as Amazon Associates, ClickBank, or Commission Junction. Create content, such as blog posts or product reviews, and include your affiliate links. Building a loyal audience and providing valuable information and recommendations are crucial for success in affiliate marketing.

Online Tutoring:
If you have expertise in a particular subject, online tutoring can be a rewarding and profitable way to make money online. Platforms like VIPKid, Tutor.com, or Chegg connect tutors with students seeking tutoring services. Create a profile showcasing your qualifications and experience, and offer your tutoring services based on your availability. Deliver high-quality instruction and provide personalized support to help students achieve their academic goals.

In conclusion, making money online offers a wealth of opportunities for individuals with diverse skills and interests. Whether through freelancing, e-commerce, blogging, online surveys, dropshipping, affiliate marketing, or online tutoring, there are numerous avenues to explore. The key to success lies in identifying your strengths, establishing a solid online presence, delivering high-quality work or content, and consistently adapting to evolving trends and technologies in the online marketplace. With dedication, perseverance, and a strategic approach, you can leverage the power of the internet to create a sustainable and profitable online income stream.
Now we will prepare this response content to pass as input to the pictory."""


def get_dict_response(gpt_response):
    gpt_response = gpt_response.replace(":\n\n", ":\n")
    formatted_text = gpt_response.split("\n\n")

    final_dict = {}
    try:
        for paragraph in formatted_text:
            lines = paragraph.replace('\n', " ")
            if 'In conclusion, ' in lines:
                lines = lines.replace('In conclusion, ', 'Conclusion: ')
            heading, *content = lines.split(': ')

            if len(content) > 1:
                content = " ".join(content)
            else:
                content = content[0]

            final_dict[heading] = content.strip('"')

        if len(final_dict['Title'] + final_dict['Subtitle']) < 100:
            final_title = final_dict.pop('Title', '') + " " + final_dict.pop('Subtitle', '')
        else:
            final_title = final_dict['Title']
            final_dict.pop('Title', '')
            final_dict.pop('Subtitle', '')

        final_content = ""

        for key, val in final_dict.items():
            each_item_content = key + ": " + val
            final_content = final_content + "\n" + each_item_content

        print("\n\nFinal Title : ", final_title, "\n\nFinal Content : ", final_content)
        return final_title, final_content
    except Exception as exp:
        print("Exception in chatGpt.py : get_dict_response() : ", exp)
