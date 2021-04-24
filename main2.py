from secmail import SecMail
from account import Account

account = Account()
account.generate_account()

print("Init TOR")
yandex = SecMail(account, open("2captcha.apikey").read())
yandex.create_account()

yandex.refresh_inbox()
print(yandex.get_page_text())
yandex.refresh_inbox()

import time
time.sleep(1000)
