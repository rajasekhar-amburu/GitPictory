from selenium import webdriver
from selenium.webdriver import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
import logging
import config
from template_ids import template_name
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpCon
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from config import *
import os
import random
import string

# Configure the logging module
logging.basicConfig(level=logging.INFO)
# Create a logger instance
logger = logging.getLogger(__name__)


# Initialize Chrome driver instance

class Pictory:

    def __init__(self,
                 topic_tile,
                 topic_content,
                 template_style,
                 driver_obj=None,
                 voice_accent='Aditi',
                 voice_speed_percentage='103',
                 background_music='off',
                 aspect_ratio='16_9',
                 download_path=None,
                 logo_path=None
                 ):
        self.voice_accent = voice_accent
        self.topic_title = topic_tile
        self.topic_content = topic_content
        self.driver_obj = driver_obj
        self.voice_speed_percentage = voice_speed_percentage
        self.background_music = background_music
        self.template_style = template_style
        self.aspect_ratio = aspect_ratio
        self.download_path = download_path
        self.logo_path = logo_path

    def exception_handler(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exp:
                print("An exception occurred : ", exp)
                logger.error("An exception occurred: {0}".format(exp))

        return wrapper

    def set_services_opitions(self):

        service = ChromeService(executable_path=ChromeDriverManager().install())

        # Configure Chrome options
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('prefs', {
            'download.default_directory': 'D:\\PictoryDownloads',
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': True
        })
        return service, chrome_options

    def open_pictory_browser(self):
        try:
            service, chrome_options = self.set_services_opitions()
            logger.info("Opening the pictory app in chrome browser")
            print("Opening the pictory app in chrome browser")
            self.driver_obj = webdriver.Chrome(service=service, options=chrome_options)
            self.driver_obj.maximize_window()

            # open to the website
            self.driver_obj.get(config.config_pictory_url)
            time.sleep(15)

            # sing-in with google account (OAuth2) - Select 'Sign-In' with Google
            pictory_signIn_with_google_xpath = '/html/body/div[2]/div[1]/div/div/div/button/p'
            self.driver_obj.find_element(By.XPATH, pictory_signIn_with_google_xpath).click()
            logger.info("Selected sign-in with google option")
            time.sleep(15)

            self.driver_obj.find_element(By.ID, 'identifierId').send_keys(config.gmail_id)
            time.sleep(2)
            self.driver_obj.find_element(By.ID, 'identifierNext').click()
            time.sleep(5)
            self.driver_obj.find_element(By.NAME, 'Passwd').send_keys(config.gmail_password)
            time.sleep(2)
            self.driver_obj.find_element(By.ID, 'passwordNext').click()
            time.sleep(25)
            logger.info("Successfully signed into google")
            print("Successfully signed into google")
        except Exception as exp:
            print("Exception occurred in pictory_selenium - open_pictory_browser", exp)

    def pictory_editor_page(self):
        try:
            time.sleep(30)  # Wait to get all components of the page loaded

            # Cick on Text to Video convertion Proceed button
            script_video_proceed_xpath = '//*[@id="root"]/div[1]/div[5]/div/div[3]/div[1]/div[1]/div[3]/button'
            self.driver_obj.find_element(By.XPATH, script_video_proceed_xpath).click()
            logger.info("Completed : Cicking on Text to Video convertion Proceed button")

            # Give Title to in the Editor page of pictory
            script_video_title_name = self.topic_title
            script_video_title_name_class = "sortof-black"
            self.driver_obj.find_element(By.CLASS_NAME, script_video_title_name_class).send_keys(
                script_video_title_name)
            logger.info("Completed : Given a title to in the Editor page of pictory")

            # Give complete content to the Editor page of pictory
            complete_script = self.topic_content
            actual_script_class = "ck-placeholder"
            self.driver_obj.find_element(By.CLASS_NAME, actual_script_class).send_keys(complete_script)
            time.sleep(20)  # Wait for text processing and enable proceed button
            logger.info("Completed : Given a content in the Editor page of pictory")

            # Click on Proceed button in the Text Content input page
            proceed_button_xpath = '//*[@id="root"]/div[1]/div[5]/div/main/div/div/div[2]/span[2]/div/div[2]/button[2]'
            self.driver_obj.find_element(By.XPATH, proceed_button_xpath).click()
            logger.info("Completed : Clicked on Proceed button in the Text Content input page")
            print("Completed : Clicked on Proceed button in the Text Content input page")
        except Exception as exp:
            print("Exception occurred in pictory_selenium - pictory_editor_page", exp)

    def choose_template(self):
        try:
            print("Waiting 20 sec to render all template")
            time.sleep(20)
            # Get the template-id for the given template-name
            template_id = template_name[self.template_style]

            if self.aspect_ratio == '16_9':
                template_aspect_ratio_xpath = '//*[@id="' + template_id + '"]/div[2]/div/div[1]/div[2]/div[1]'
            elif self.aspect_ratio == "9_16":
                template_aspect_ratio_xpath = '//*[@id="' + template_id + '"]/div[2]/div/div[1]/div[2]/div[2]'
            else:
                template_aspect_ratio_xpath = '//*[@id="' + template_id + '"]/div[2]/div/div[1]/div[2]/div[3]'

            logger.info("Selected aspect-ratio as {0} for the scene".format(self.aspect_ratio))

            time.sleep(15)
            self.driver_obj.find_element(By.ID, template_id).click()
            self.driver_obj.find_element(By.XPATH, template_aspect_ratio_xpath).click()
            print("Selected the given template : ", self.template_style,
                  " waiting 120 sec to redirect to video editing page")
            time.sleep(120)
        except Exception as exp:
            print("Exception occurred in pictory_selenium - choose_template", exp)

    def close_offer_pop_up(self):
        try:
            self.driver_obj.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            print("Closed the popup.")
        except NoSuchElementException:
            print("Popup close button not found.")

    def click_watermark_got_it(self):
        try:
            # Close the black-friday popup
            self.close_offer_pop_up()

            # Click on Got-It button in the initial scenes section
            watermark_gotIt_xpath = '//*[@id="Scene_2_1"]/div[3]/div[1]/div[2]/div/button'
            self.driver_obj.find_element(By.XPATH, watermark_gotIt_xpath).click()
            logger.info("Completed : Clicking on Got-It button in the initial scenes section")
            print("Completed : Clicking on Got-It button in the initial scenes section")
        except Exception as exp:
            print("Exception occurred in pictory_selenium - click_watermark_got_it", exp)

    def apply_person_voice(self):
        try:
            # Select Icons on the left side of the window
            audio_menu_tile_xpath = '//*[@id="side-navbar"]/ul/li[3]/a/h4'
            voice_over_tab_xpath = '//*[@id="tab-3"]/div/ul/li[2]'
            self.driver_obj.find_element(By.XPATH, audio_menu_tile_xpath).click()
            self.driver_obj.find_element(By.XPATH, voice_over_tab_xpath).click()
            logger.info("Video Edit page : Navigation from Audio -> VoiceOver")

            # voic-track id of a person accent choosen
            voice_of_person = self.voice_accent
            if voice_of_person == 'Aditi':
                x_person_voice_track_id = "voiceTrack1010"  # this is for aditi
            elif voice_of_person == 'Freya':
                x_person_voice_track_id = "voiceTrack3023"
            x_person_voice_track_apply_click1_xpath = '//*[@id="' + x_person_voice_track_id + '"]'
            x_person_voice_track_apply_click2_xpath = '//*[@id="' + x_person_voice_track_id + '"]/div[2]/div/span'

            # clear the search voice text area and enter the person name
            search_input = self.driver_obj.find_element(By.CSS_SELECTOR, 'input[placeholder="Search voices"]')
            search_input.clear()
            search_input.send_keys(voice_of_person)
            time.sleep(5)
            logger.info("Audio -> VoiceOver -> Search -> {0}".format(voice_of_person))

            # hover to the resulted person name and click apply button
            click1 = self.driver_obj.find_element(By.XPATH, x_person_voice_track_apply_click1_xpath)
            click2 = self.driver_obj.find_element(By.XPATH, x_person_voice_track_apply_click2_xpath)
            actions = ActionChains(self.driver_obj)
            actions.click(click1).click(click2).perform()
            logger.info("Audio -> VoiceOver -> Search -> {0} -> Apply & wait 90 sec".format(voice_of_person))
            time.sleep(90)  # Wait to apply the voice

            # Click on Settings Icon in the Scene section
            settings_button_id = 'dropdownMenu2'
            self.driver_obj.find_element(By.ID, settings_button_id).click()

            # Apply the person voice to all scenes / slides
            x_person_voic_apply_to_all_xpath = '//*[@id="scene-setting-dropdown"]/ul/li[6]/input'
            self.driver_obj.find_element(By.XPATH, x_person_voic_apply_to_all_xpath).click()
            logger.info("Apply {0} voice to all scenes & wait for 30 sec".format(voice_of_person))
            time.sleep(30)
        except Exception as exp:
            print("Exception occurred in pictory_selenium - apply_person_voice", exp)

    @exception_handler
    def adjust_voice_speed(self):

        audio_menu_tile_xpath = '//*[@id="side-navbar"]/ul/li[3]/a/h4'
        voice_over_tab_xpath = '//*[@id="tab-3"]/div/ul/li[2]'

        self.driver_obj.find_element(By.XPATH, audio_menu_tile_xpath).click()
        self.driver_obj.find_element(By.XPATH, voice_over_tab_xpath).click()
        time.sleep(2)

        speed_control_drop_down_xpath = '//*[@id="speed-container-span"]/div[1]'
        voice_over_speed_current_value_xpath = '//*[@id="speed-container-span"]/div[2]/div/div/div/span/span/span'

        self.driver_obj.find_element(By.ID, "speed-container-span").click()
        current_value_element = self.driver_obj.find_element(By.XPATH, voice_over_speed_current_value_xpath)

        # Ensure the desired value is within the valid range
        desired_value = max(50, min(200, int(self.voice_speed_percentage)))

        # "arguments[0].innerText = '{}%';".format(desired_value): This is the JavaScript code that will be executed.
        # arguments[0] refers to the first argument passed to the JavaScript function. In this case, it's the element
        # referenced by current_value_element. .innerText is a property of the element that represents the text
        # content within the element.
        self.driver_obj.execute_script("arguments[0].innerText = '{}%';".format(desired_value), current_value_element)
        self.driver_obj.find_element(By.ID, "speed-container-span").click()
        time.sleep(15)  # wait to apply speed

    def customize_background_music(self):
        try:
            # Click on Settings Icon in the Scene section
            settings_button_id = 'dropdownMenu2'
            self.driver_obj.find_element(By.ID, settings_button_id).click()

            # Apply / Disable the background music to all scenes
            background_music_slider_xpath = '//*[@id="scene-setting-dropdown"]/ul/li[8]/label/span'
            background_music_apply_all_xpath = '//*[@id="scene-setting-dropdown"]/ul/li[8]/input'
            self.driver_obj.find_element(By.XPATH, background_music_slider_xpath).click()
            self.driver_obj.find_element(By.XPATH, background_music_apply_all_xpath).click()
            logger.info("Disable the background music to all scenes & wait 10 sec")
            print("Disable the background music to all scenes & wait 10 sec")
            time.sleep(10)  # Time to apply all scenes
        except Exception as exp:
            print("Exception occurred in pictory_selenium - customize_background_music", exp)

    def prepare_video_download(self):
        try:
            generate_video_download_button_id = 'generate-button-dropdown'
            self.driver_obj.find_element(By.ID, generate_video_download_button_id).click()

            download_as_video_button_id = 'btnGenerate'
            self.driver_obj.find_element(By.ID, download_as_video_button_id).click()
            logger.info(
                "Clicked on Download video button in Editor page to generate downloadable video & waiting for 7 min")
            print("Clicked on Download video button in Editor page to generate downloadable video & waiting for 7 min")
            time.sleep(420)
        except Exception as exp:
            print("Exception occurred in pictory_selenium - prepare_video_download", exp)

    def final_video_preview(self):
        try:
            final_video_preview_button_id = 'btnPreview'
            self.driver_obj.find_element(By.ID, final_video_preview_button_id).click()
            time.sleep(90)
        except Exception as exp:
            print("Exception occurred in pictory_selenium - final_video_preview", exp)

    def final_video_download(self):

        time.sleep(2)  # wait to render the page
        download_button = WebDriverWait(self.driver_obj, 10).until(
            ExpCon.element_to_be_clickable((By.XPATH, '//button[text()="Download"]')))
        download_button.click()
        logger.info("Clicked on Download Video button to download the video into local system & waiting for 90 sec")
        print("Clicked on Download Video button to download the video into local system & waiting for 90 sec")
        time.sleep(90)

    def stop_looping_same_visual(self):
        try:
            # Click on Settings Icon in the Scene section
            settings_button_id = 'dropdownMenu2'
            self.driver_obj.find_element(By.ID, settings_button_id).click()

            loop_video_slider_xpath = '//*[@id="scene-setting-dropdown"]/ul/li[3]/label/span'
            loop_video_apply_all_xpath = '//*[@id="scene-setting-dropdown"]/ul/li[3]/input'
            self.driver_obj.find_element(By.XPATH, loop_video_slider_xpath).click()
            self.driver_obj.find_element(By.XPATH, loop_video_apply_all_xpath).click()
            logger.info("Selected : Stop looping the same visual in the scenes")
            print("Selected : Stop looping the same visual in the scenes")
            time.sleep(10)  # Time to apply all scenes
        except Exception as exp:
            print("Exception occurred in pictory_selenium - stop_looping_same_visual", exp)

    def generate_random_name(self, length=10):
        characters = string.ascii_letters + string.digits
        random_name = ''.join(random.choice(characters) for _ in range(length))
        random_name = ''
        for _ in range(length):
            randChar = random.choice(characters)
            random_name += randChar
        return random_name
    def delete_logo_template(self):
        try:
            branding_menu_xpath = '//*[@id="side-navbar"]/ul/li[7]'
            branding_scene_xpath = '//*[@id="scenes"]'
            self.driver_obj.find_element(By.XPATH, branding_menu_xpath).click()
            time.sleep(2)
            self.driver_obj.find_element(By.XPATH, branding_scene_xpath).click()
            time.sleep(2)

            # Delete the first template present in my-templates
            logger.info("Navigating to choose-template to delete the logo template under my-templates")
            print("Navigating to choose-template to delete the logo template under my-templates")

            change_template_xpath = '//*[@id="templates-main"]/div/div/div/div/div/div[1]/div/div[1]/div[2]/button[1]'
            self.driver_obj.find_element(By.XPATH, change_template_xpath).click()
            time.sleep(5)
            my_template_button_xpath = '//*[@id="template_tab_2"]'
            self.driver_obj.find_element(By.XPATH, my_template_button_xpath).click()
            time.sleep(5)
            logger.info("Navigated to my-templates")
            print("Navigated to my-templates")

            try:
                wait = WebDriverWait(self.driver_obj, 10)
                tile_xpath = '//*[@id="templatesGrid"]/div[2]/div/div[1]/div'
                tile_element = wait.until(ExpCon.element_to_be_clickable((By.XPATH, tile_xpath)))
                ActionChains(self.driver_obj).move_to_element(tile_element).perform()
                delete_first_template_xpath = '//*[@id="templatesGrid"]/div[2]/div/div[1]/div/div[2]/div[2]/div/div/button'
                button_element = wait.until(ExpCon.element_to_be_clickable((By.XPATH, delete_first_template_xpath)))
                button_element.click()
                logger.info("Navigated to my-templates - Selected the first tile")
                print("Navigated to my-templates - Selected the first tile")
            except Exception as expt:
                logger.info("Exception occurred when deleting the first-template-tile under my templates")
                print("Exception occurred when deleting the first-template-tile under my templates :", expt)

            close_template_popup_xpath = '//*[@id="templates-modal"]/div/button'
            self.driver_obj.find_element(By.XPATH, close_template_popup_xpath).click()
            logger.info("Completed : Deleted the logo template from my-template")
            print("Completed : Deleted the logo template from my-template")
        except Exception as exp:
            print("Exception occurred at pictory_selenium - delete_logo_template :", exp)


    def apply_branding_logo(self):
        try:
            self.delete_logo_template()

            branding_menu_xpath = '//*[@id="side-navbar"]/ul/li[7]'
            branding_scene_xpath = '//*[@id="scenes"]'
            self.driver_obj.find_element(By.XPATH, branding_menu_xpath).click()
            time.sleep(2)
            self.driver_obj.find_element(By.XPATH, branding_scene_xpath).click()
            time.sleep(2)

            upload_logo_xpath = '//*[@id="scenes-in-templates-div"]/div/div/div[2]/div/div/div[2]/label/input'
            file_input = self.driver_obj.find_element(By.XPATH, upload_logo_xpath)
            file_input.send_keys(self.logo_path)
            time.sleep(15)

            try:
                template_title_xpath = '//*[@id="templates-main"]/div/div/div/div/div/div[1]/div/div[1]/div[1]/div/span/div[2]/div/input'
                template_input = self.driver_obj.find_element(By.XPATH, template_title_xpath)
                template_title = self.generate_random_name()
                template_input.click()
                template_input.clear()
                template_input.send_keys(template_title)
                time.sleep(5)
                print("Changed the template title.")
            except Exception as expt:
                print("Exception occurred in pictory_selenium. Unable to change the template title.")

            ####### Logo Size Change ########
            logo_size_slider_xpath = '//*[@id="scenes-in-templates-div"]/div/div/div[2]/div[2]/div[2]/span[1]/span[2]'
            logo_size_input_xpath = '//*[@id="scenes-in-templates-div"]/div/div/div[2]/div[2]/div[2]/span[1]/span[3]/input'

            # Wait for the slider to be present on the page
            slider = WebDriverWait(self.driver_obj, 10).until(
                ExpCon.presence_of_element_located((By.XPATH, logo_size_slider_xpath))
            )

            # Set the desired value '10'
            desired_value = '10'

            # Update the value attribute of the input element
            input_element = self.driver_obj.find_element(By.XPATH, logo_size_input_xpath)
            self.driver_obj.execute_script("arguments[0].setAttribute('value', '{}')".format(desired_value),
                                           input_element)

            # Trigger the input event to update the slider
            self.driver_obj.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                                           input_element)

            # Re-locate the slider element after the dynamic update
            slider = WebDriverWait(self.driver_obj, 10).until(
                ExpCon.presence_of_element_located((By.XPATH, logo_size_slider_xpath))
            )

            # Click the slider to apply the changes
            ActionChains(self.driver_obj).click(slider).perform()
            time.sleep(10)
            logger.info("Logo size changed")
            print("Logo size changed")

            #################### Logo Opacity Change ##################
            logo_opacity_slider_xpath = '//*[@id="scenes-in-templates-div"]/div/div/div[2]/div[2]/div[2]/span[2]/span[2]'
            logo_opacity_input_xpath = '//*[@id="scenes-in-templates-div"]/div/div/div[2]/div[2]/div[2]/span[2]/span[3]/input'

            # Wait for the slider to be present on the page
            slider = WebDriverWait(self.driver_obj, 10).until(
                ExpCon.presence_of_element_located((By.XPATH, logo_opacity_slider_xpath))
            )

            # Set the desired value '10'
            desired_value = '50'

            # Update the value attribute of the input element
            input_element = self.driver_obj.find_element(By.XPATH, logo_opacity_input_xpath)
            self.driver_obj.execute_script("arguments[0].setAttribute('value', '{}')".format(desired_value),
                                           input_element)

            # Trigger the input event to update the slider
            self.driver_obj.execute_script("arguments[0].dispatchEvent(new Event('input', { bubbles: true }));",
                                           input_element)

            # Re-locate the slider element after the dynamic update
            slider = WebDriverWait(self.driver_obj, 10).until(
                ExpCon.presence_of_element_located((By.XPATH, logo_opacity_slider_xpath))
            )

            # Click the slider to apply the changes
            ActionChains(self.driver_obj).click(slider).perform()
            time.sleep(10)
            logger.info("Logo Opacity changed")
            print("Logo Opacity changed")

            # Place the logo on top right corner
            logo_position_xpath = '//*[@id="scenes-in-templates-div"]/div/div/div[2]/div[2]/div[1]/span/div'
            top_right_corner_xpath = '/html/body/div[2]/div[1]/div[3]/div[8]/main/section/div/div[1]/div/div[4]/div/div/div/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[2]/div[1]/span/div/div[3]'
            self.driver_obj.find_element(By.XPATH, logo_position_xpath).click()
            self.driver_obj.find_element(By.XPATH, top_right_corner_xpath).click()
            logger.info("Placed the logo in the top-right corner")
            print("Placed the logo in the top-right corner")
            time.sleep(5)
        except Exception as exp:
            print("Exception occurred in pictory_selenium - apply_branding_logo :", exp)

    def customize_video(self):

        self.click_watermark_got_it()

        self.apply_person_voice()

        if self.voice_speed_percentage != '100':
            self.adjust_voice_speed()

        self.apply_branding_logo()

        self.customize_background_music()

        self.stop_looping_same_visual()

    def youtube_upload(self,
                       file_path,
                       title,
                       description,
                       keywords='',
                       privacy_status="public"):
        try:
            # Execute JavaScript to open a new tab
            self.driver_obj.execute_script("window.open('');")

            # Switch to the new tab (index starts with 0)
            self.driver_obj.switch_to.window(self.driver_obj.window_handles[1])

            self.driver_obj.get("https://studio.youtube.com")
            time.sleep(10)

            upload_button = self.driver_obj.find_element(By.XPATH, '//*[@id="upload-icon"]')
            upload_button.click()
            time.sleep(2)

            file_input = self.driver_obj.find_element(By.XPATH, '//*[@id="content"]/input')
            file_input.send_keys(file_path)
            time.sleep(75)

            title_input = self.driver_obj.find_element(By.XPATH, '//*[@id="textbox"]')
            title_input.click()
            title_input.clear()
            title_input.send_keys(title)
            time.sleep(5)

            description_input = self.driver_obj.find_element(By.ID, 'description-textarea')
            description_input.send_keys(description)
            time.sleep(10)

            self.driver_obj.find_element(By.NAME, "VIDEO_MADE_FOR_KIDS_NOT_MFK").click()
            time.sleep(2)

            self.driver_obj.find_element(By.CLASS_NAME, 'expand-button').click()
            time.sleep(2)

            self.driver_obj.find_element(By.NAME, 'VIDEO_AGE_RESTRICTION_NONE').click()
            time.sleep(2)

            # show more - for tags
            self.driver_obj.find_element(By.XPATH, '//*[@id="toggle-button"]/div').click()
            time.sleep(2)

            tags_full_xpath = '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-advanced/div[5]/ytcp-form-input-container/div[1]/div/ytcp-free-text-chip-bar/ytcp-chip-bar/div/input'
            tags_container = self.driver_obj.find_element(By.XPATH, tags_full_xpath)
            tags_container.click()
            tags_container.send_keys(keywords)
            time.sleep(5)

            # click outside the text area to set all tags properly
            self.driver_obj.find_element(By.XPATH, '//*[@id="tags-instruction"]').click()

            details_page_next_button = self.driver_obj.find_element(By.XPATH, '//*[@id="next-button"]')
            details_page_next_button.click()
            time.sleep(5)

            video_elements_next_button = self.driver_obj.find_element(By.XPATH, '//*[@id="next-button"]')
            video_elements_next_button.click()
            time.sleep(5)

            checks_next_button = self.driver_obj.find_element(By.XPATH, '//*[@id="next-button"]')
            checks_next_button.click()
            time.sleep(10)

            visibility = self.driver_obj.find_element(By.NAME, privacy_status.upper())
            visibility.click()
            time.sleep(5)

            publish_button = self.driver_obj.find_element(By.XPATH, '//*[@id="done-button"]')
            publish_button.click()
            print("**** Published the video *****")
            time.sleep(30)

            close_published_pop_up = self.driver_obj.find_element(By.XPATH, '//*[@id="close-button"]/div')
            close_published_pop_up.click()
            print("**** Closing the published pop-up *****")

        except Exception as exp:
            print("Exception occurred in pictory_selenium - youtube_upload : ", exp)

    def close_browser(self):
        try:
            print("******* Closing the chrome browser ********")
            self.driver_obj.quit()
        except Exception as exp:
            print("Exception occurred in pictory_selenium - close_browser :", exp)
