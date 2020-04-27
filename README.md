# JLU_AUTO_SUBMISSION

Automatic health report submission for JLU

# Requirments

- Chrome v81
- Chrome Driver v81
- python3
- Selenium

Simple configuration is required, just Google it.

# Usage

## Basic usage

Please fill in the `username` and `password` in line 9 and 10 of `submit.py`.

If you want to save the log, you can fill in `logpath` in line 12, otherwise please keep it as an empth string.

```python
# personal info
username = "XXX"
password =  "XXX"
logpath = r""
```

Then you can run `submit.py` to check the result.

## Advanced usage

- Headless mode
- Submit regularly
    - For Windows, you can use `Task Scheduler` to submit regularly.
    - For Linux/Unix, you can use `crontab` to submit regularly.
    - Tips: It is recommended to set the trigger to 1 AM or 2 AM to avoid peak traffic.

# Known Issue

- Incomplete Autofill #1

Please use xpath to fill in these items manually.

```python
ele = browser.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[1]/table/tbody/tr[2]/td/div/table/tbody/tr[34]/td[4]/div/div/div/div/input')
ele.send_keys("上海市")
ele.send_keys(Keys.ENTER)
```

These codes should be inserted between lines 30 and 34.

# Future

- Automatic notification
    - Use E-mail, WeChat, et al. to automatically notify.
