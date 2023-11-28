from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
import script_content_ChatGpt

service=ChromeService(executable_path=ChromeDriverManager().install())
# Initialize Chrome driver instance

with webdriver.Chrome(service=service) as driver:


    driver.get('https://www.gmail.com/')
    #Google Sign-In
    driver.find_element(By.ID, 'identifierId').send_keys('mysnapstoies@gmail.com')
    time.sleep(2)
    driver.find_element(By.ID, 'identifierNext').click()
    time.sleep(2)
    driver.find_element(By.NAME, 'Passwd').send_keys('09Oct91.')
    time.sleep(2)
    driver.find_element(By.ID, 'passwordNext').click()
    time.sleep(5)

    # Open new window
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get('https://platform.openai.com/login?launch')
    #time.sleep(15)

    from autoGUI import record_actions, replay_actions

    record_actions()
    #open_ai_menu_xpath = '//*[@id="home"]/div[1]/div[1]/div[2]/header/div[1]/div/div[3]/button/span/span'
    #driver.find_element(By.XPATH, open_ai_menu_xpath).click()

    driver.maximize_window()
    open_ai_login_xpath = "/html/body/div/div[2]/div/div[1]/div[1]/div[1]/div[2]/header/div[2]/div/div/div/div/nav[2]/ul/li[1]/a/span/span"
    driver.find_element(By.XPATH, open_ai_login_xpath).click()

    #driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])
    #driver.get('https://platform.openai.com/login?launch')

    open_ai_chat_gpt_redirect_xpath = "/html/body/div[1]/div[1]/div/div/div[2]/a[1]"
    driver.find_element(By.XPATH, open_ai_chat_gpt_redirect_xpath).click()

    open_ai_continue_google_xpath = "/html/body/div/main/section/div/div/div/div[4]/form[2]/button/span[2]"
    driver.find_element(By.XPATH, open_ai_continue_google_xpath).click()


    chat_gpt_login_button_xpath = '//*[@id="root"]/div[1]/div/div/div[2]/a[1]'
    driver.find_element(By.XPATH, chat_gpt_login_button_xpath).click()

    driver.find_element(By.ID, "challenge-stage").click()

