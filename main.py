from secmail import SecMail
from account import Account

account = Account()
account.generate_account()

yandex = SecMail(account, open("2captcha.apikey").read())
yandex.create_account()

import time
time.sleep(1000)
