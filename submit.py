from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import itertools
import time

# personal info
username = "XXX"
password =  "XXX"

def submit_form(count):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--log-level=3")
    browser = webdriver.Chrome(options = chrome_options)
    browser.set_page_load_timeout(1000)
    flag = False
    try:
        # home page
        browser.get("https://ehall.jlu.edu.cn/")
        # login
        browser.find_element_by_id("username").send_keys(username)
        browser.find_element_by_id("password").send_keys(password)
        browser.find_element_by_id("login-submit").click()
        # submission page
        browser.get("https://ehall.jlu.edu.cn/infoplus/form/JLDX_YJS_XNYQSB/start")
        # check checkbox & submit
        WebDriverWait(browser,60,2).until(EC.presence_of_element_located((By.NAME,"fieldCNS")))
        browser.find_element_by_name("fieldCNS").click()
        browser.find_element_by_xpath("//*[@id='form_command_bar']/li[1]/a[1]").click()
        # pop-up window
        WebDriverWait(browser,60,2).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"备注")))
        browser.find_element_by_css_selector("[class='dialog_button default fr']").click()
        # check
        time.sleep(5)
        if browser.page_source.find("办理成功") != -1:
            flag = True
    except:
        print("Error!")
    finally:
        if flag:
            print ("Submission {}: Success".format(count))
        else:
            print ("Submission {}: Failure".format(count))
        browser.close()
        return flag

if __name__=="__main__":
    count = 0
    while count < 11:
        count += 1
        if submit_form(count):
            break
