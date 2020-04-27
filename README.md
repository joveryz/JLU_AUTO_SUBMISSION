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

Please fill in the `username` and `password` on line 9 and 10 of `submit.py`.

```
# personal info
username = "XXX"
password =  "XXX"
```

Then you can run `submit.py` to check the result.

## Advanced usage

- Headless mode
- Submit regularly
    - For Windows, you can use `Task Scheduler` to submit regularly.
    - For Linux/Unix, you can use `crontab` to submit regularly.
    - Tips: It is recommended to set the trigger to 1 AM or 2 AM to avoid peak traffic.

# Future

- Automatic notification
    - Use E-mail, WeChat, et al. to automatically notify.
