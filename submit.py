from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import itertools
import requests
import time
import json

# personal info
username = "XXX"
password =  "XXX"
logpath = r""

# Push
secret = ""
corpID = ""
agentID = ""
pushuser = ""
flag = False


def write_log(logstr):
    global logpath
    if logpath != "":
        with open (logpath,'a+')as f:
            f.write (logstr + "\n")
        f.close()

def push_wechat():
    global flag, secret, corpID, agentID
    tokenUrl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}"
    postUrl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}"
    req = requests.get(url=tokenUrl.format(corpID,secret))
    acctoken = req.json().get('access_token')
    constr = "{} Success".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    if not flag:
        constr = constr.replace("Success", "Failure")
    pushdata = {
        "touser" : pushuser,
        "msgtype" : "text",
        "agentid" : agentID,
        "text" : {
            "content" : constr
        },
        "safe":0
    }
    ret = requests.post(url=postUrl.format(acctoken),data=json.dumps(pushdata))
    if ret.json()["errcode"] == 0:
        write_log("WeChat pushed successfully: " + constr)
    else:
        write_log("WeChat pushed failed: " + constr)
        write_log("Push error: " + str(ret.json()))

def submit_form(count):
    global flag, username, password, logpath
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--log-level=3")
    browser = webdriver.Chrome(options = chrome_options)
    browser.set_page_load_timeout(1000)
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
        #ele = browser.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr[34]/td[4]/div/div/div/div/input')
        #ele.send_keys("上海市")
        #ele.send_keys(Keys.ENTER)
        browser.find_element_by_name("fieldCNS").click()
        browser.find_element_by_xpath("//*[@id='form_command_bar']/li[1]/a[1]").click()
        # pop-up window
        WebDriverWait(browser,60,2).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"备注")))
        browser.find_element_by_css_selector("[class='dialog_button default fr']").click()
        # check
        time.sleep(5)
        if browser.page_source.find("办理成功") != -1:
            flag = True
    except Exception as e:
        print(e)
        write_log("Submit error: " + str(e))
    finally:
        browser.close()
        logstr = "{} Submission {}: Success".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), count)
        if not flag:
            logstr = logstr.replace("Success", "Failure")
        write_log(logstr)
        print(logstr)
        return flag

if __name__=="__main__":
    count = 0
    while count < 11:
        count += 1
        if submit_form(count):
            break
    if secret != "":
        push_wechat()
