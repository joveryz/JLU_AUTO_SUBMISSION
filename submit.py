from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import itertools
import requests
import time
import json
import sys

# personal info
username = ["XXX", "XXX"]
password = ["XXX", "XXX"]
logpath = r""

# Push
secret = ""
corpID = ""
agentID = ""
toUser = ""

# Others
status = []
dataformat = "%Y-%m-%d %H:%M:%S"

def write_log(logstr):
    print(logstr)
    global logpath
    if logpath != "":
        with open (logpath,'a+')as f:
            f.write (logstr + "\n")
        f.close()

def push_wechat():
    global secret, corpID, agentID, toUser
    tokenUrl = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}"
    postUrl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}"
    req = requests.get(url=tokenUrl.format(corpID,secret))
    acctoken = req.json().get('access_token')
    pushstr = "{} Auto Submit: ".format(time.strftime(dataformat, time.localtime()))
    for index in range(len(username)):
        if status[index]:
            pushstr += "{}(Success), ".format(username[index])
        else:
            pushstr += "{}(Failure), ".format(username[index])
    pushstr = pushstr[:-2]
    pushdata = {
        "touser" : toUser,
        "msgtype" : "text",
        "agentid" : agentID,
        "text" : {
            "content" : pushstr
        },
        "safe":0
    }
    write_log("{} Auto Submit: [WeChat Str] {}".format(time.strftime(dataformat, time.localtime()), pushstr))
    ret = requests.post(url=postUrl.format(acctoken),data=json.dumps(pushdata))
    pushlog = "{} Auto Submit: [WeChat Info] Success".format(time.strftime(dataformat, time.localtime()))
    if ret.json()["errcode"] != 0:
        write_log("{} Auto Submit: [WeChat Error] {}".format(time.strftime(dataformat, time.localtime()), str(ret.json()).replace("\n","-")))
        pushlog = pushlog.replace("Success", "Failure")
    write_log(pushlog)

def submit_form(index):
    global username, password, status, logpath
    if status[index]:
        return
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument("--log-level=3")
    browser = webdriver.Chrome(options = chrome_options)
    browser.set_page_load_timeout(30)
    try:
        # home page
        browser.get("https://ehall.jlu.edu.cn/")
        # login
        browser.find_element_by_id("username").send_keys(username[index])
        browser.find_element_by_id("password").send_keys(password[index])
        browser.find_element_by_id("login-submit").click()
        # submission page
        browser.get("https://ehall.jlu.edu.cn/infoplus/form/JLDX_YJS_XNYQSB/start")
        # check checkbox & submit
        WebDriverWait(browser,30,2).until(EC.presence_of_element_located((By.NAME,"fieldCNS")))
        #ele = browser.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr[34]/td[4]/div/div/div/div/input')
        #ele.send_keys("上海市")
        #ele.send_keys(Keys.ENTER)
        browser.find_element_by_name("fieldCNS").click()
        browser.find_element_by_xpath("//*[@id='form_command_bar']/li[1]/a[1]").click()
        # pop-up window
        WebDriverWait(browser,30,2).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"备注")))
        browser.find_element_by_css_selector("[class='dialog_button default fr']").click()
        # check
        time.sleep(5)
        if browser.page_source.find("办理成功") != -1:
            status[index] = True
        else:
            status[index] = False
    except Exception as e:
        write_log("{} Auto Submit: [Submit Error {}] {}".format(time.strftime(dataformat, time.localtime()), username[index], str(e).replace("\n","-")))
    finally:
        browser.close()
        logstr = "{} Auto Submit: [Submit Info {}] Success".format(time.strftime(dataformat, time.localtime()), username[index])
        if not status[index]:
            logstr = logstr.replace("Success", "Failure")
        write_log(logstr)
        return

if __name__=="__main__":
    count = 0
    for index in range(len(username)):
            status.append(False)
    while count < 1:
        count += 1
        for index in range(len(username)):
            submit_form(index)
    if secret != "":
        push_wechat()
    for index in range(len(username)):
        if not status[index]:
            sys.exit(1)
    sys.exit(0)