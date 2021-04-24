import inspect
import os
import random

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import base64
import requests
from webdriver import TorDriver, TorDriver2, WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


# class SecMail(WebDriver):
class SecMail(TorDriver):

    def __init__(self, account=None, api_key=None):
        print("Init SecMail with TOR")
        opts = Options()
        opts.add_experimental_option('prefs', {'intl.accept_languages': 'tr-TR,tr;q=0.8,en-US;q=0.6,en;q=0.4'})
        opts.add_argument(
            '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
        opts.add_argument(
            '--proxy-server="socks5://localhost:9050"')
        TorDriver2.__init__(self, opts)
        self.registerPage = 'http://secmail63sex4dfw6h2nsrbmfz2z6alwxe4e3adtkpd4pcvkhht4jdad.onion/src/signup.php' 
        # self.registerPage = 'https://myip.ru/'
        self.apiKey = api_key
        self.account = account
        self.id = None
        self.captcha = b''
        self.registered_stats = "No email registered"
        self.account.password = "aaaaaaaa1."
        
        def interceptor(request, response):  # A response interceptor takes two args
            if 'captcha.php' in request.url:
                self.captcha = response.body

        self.driver.response_interceptor = interceptor

    def create_account(self):
        self.driver.get(self.registerPage)
        time.sleep(2)

        try:
            self.wait_until_page_loaded()

            # first_name_element = self.get_element(By.ID, 'firstname')
            # last_name_element = self.get_element(By.ID, 'lastname')
            # login_element = self.get_element(By.CSS_SELECTOR, 'body > div:nth-child(1) > form:nth-child(5) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(2) > input:nth-child(1)')
            login_element = self.get_element(By.NAME, 'register_email')

            # self.send_slow_key(first_name_element, self.account.firstName)

            # self.send_slow_key(last_name_element, self.account.lastName)

            self.account.mail += ''.join([str(random.randint(0,9)), str(random.randint(0,9))])
            self.email_addr = self.account.mail + '@secmail.pro' 
            self.send_slow_key(login_element, self.account.mail)

            # self.wait_until_ajax_response()
            # time.sleep(1)

            # password_element = self.get_element(By.ID, 'password')
            password_element = self.get_element(By.NAME, 'register_secretkey')
            self.send_slow_key(password_element, self.account.password)

            password_confirm_element = self.get_element(By.NAME, 'register_confirmSecretkey')
            self.send_slow_key(password_confirm_element, self.account.password)

            self.registered_stats = ('Email adresi {}@secmail.pro ve sifre {} olarak belirlendi'.format(
               self.account.mail, self.account.password))
            print("Trying with", self.registered_stats)

            self.fill_other_fields()

        finally:
            print(self.registered_stats)
            # self.driver.quit()
            pass

    def decode_capthca(self, selector="#captcha_image"):
        print('Capthca cozuluyor')

        b64_captcha = self.driver.execute_script(f"""
var canvas = document.createElement('canvas');
var context = canvas.getContext('2d');
var img = document.querySelector('{selector}');
canvas.height = img.naturalHeight;
canvas.width = img.naturalWidth;
context.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight);
var base64String = canvas.toDataURL();
return base64String;
        """);
        # print("CAPTCHA IMAGE:", b64_captcha)

        # b64_captcha = base64.b64encode(self.captcha)
        text = ""
        # text = input("Captcha answer:")
        if not text:
            id_result = requests.post("http://2captcha.com/in.php",
                                    data={'method': "base64", 'key': self.apiKey, 'body': b64_captcha, 'json': 0}).text

            id_result = id_result.split('|')
            self.id = id_result[1]

            print('Captcha id: ' + self.id)

            text_result = requests.get("http://2captcha.com/res.php?key=" + self.apiKey + "&action=get&id=" + self.id).text

            captcha_retry_count = 0

            while text_result == 'CAPCHA_NOT_READY' and captcha_retry_count < 5:
                print('Captcha is not ready, waiting')
                time.sleep(60)
                text_result = requests.get(
                    "http://2captcha.com/res.php?key=" + self.apiKey + "&action=get&id=" + self.id).text
                captcha_retry_count += 1
                if captcha_retry_count == 5:
                    self.driver.quit()
            print(text_result)
            text = text_result.split('|')
            text = text[1]

        print('Captcha cozuldu {}'.format(text))

        captcha_element = self.get_element(By.NAME, 'captcha')
        captcha_element.clear()
        self.send_slow_key(captcha_element, text.upper())

    def fill_other_fields(self):
        self.decode_capthca()
        time.sleep(5)
        # time.sleep(1000)
        try:
            confirm_registration_element = self.get_element(By.CSS_SELECTOR, 'input[type="submit"]')
            confirm_registration_element.click()
        except:
            self.driver.execute_script("return document.querySelector('input[type=\"submit\"]').click();")
        # self.wait_until_ajax_response()
        self.wait_until_page_loaded()



        login_element = self.get_element(By.NAME, 'register_email')
        self.send_slow_key(login_element, self.account.mail)
        password_element = self.get_element(By.NAME, 'register_secretkey')
        self.send_slow_key(password_element, self.account.password)
        password_confirm_element = self.get_element(By.NAME, 'register_confirmSecretkey')
        self.send_slow_key(password_confirm_element, self.account.password)

        self.decode_capthca()
        time.sleep(5)
        # time.sleep(1000)
        try:
            confirm_registration_element = self.get_element(By.CSS_SELECTOR, 'input[type="submit"]')
            confirm_registration_element.click()
        except:
            self.driver.execute_script("return document.querySelector('input[type=\"submit\"]').click();")
        # self.wait_until_ajax_response()
        self.wait_until_page_loaded()

        try:
            confirm_registration_element = self.get_element(By.CSS_SELECTOR, 'body > div:nth-child(1) > form:nth-child(5) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)')
            print("Captcha unsolved")
            self.driver.quit()
            raise Exception("Could not solve captcha")
        except:
            pass
        
        ret = self.driver.execute_script('return document.querySelector("body > div:nth-child(1) > form:nth-child(5) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2)")')
        if ret:
            print("Captcha unsolved")
            self.driver.quit()
            raise Exception("Could not solve captcha")

        self.driver.get("http://secmail63sex4dfw6h2nsrbmfz2z6alwxe4e3adtkpd4pcvkhht4jdad.onion/src/login.php")
        self.wait_until_page_loaded()
        login_element = self.get_element(By.NAME, 'login_username')
        self.send_slow_key(login_element, self.account.mail)
        password_element = self.get_element(By.NAME, 'secretkey')
        self.send_slow_key(password_element, self.account.password)
        self.decode_capthca(selector='body > div:nth-child(1) > form:nth-child(7) > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(3) > td:nth-child(1) > img:nth-child(1)')
        confirm_registration_element = self.get_element(By.CSS_SELECTOR, 'input[type="submit"]')
        confirm_registration_element.click()


    def refresh_inbox(self):
        "Refresh the inboxes. Don't forget to add delay to wait for reload"
        # document.getElementsByTagName("frame")[0].contentDocument.querySelector("body > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(3) > b:nth-child(2) > a:nth-child(1)").click()
        try:
            self.driver.execute_script('document.getElementsByTagName("frame")[0].contentDocument.querySelector("body > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(3) > b:nth-child(2) > a:nth-child(1)").click()');
        except:
            self.driver.execute_script('document.getElementsByTagName("frame")[0].contentDocument.querySelector("body > table:nth-child(5) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(3) > a:nth-child(2)").click()');

        self.wait_until_page_loaded()
    
    def select_inbox(self):
        "Select inbox folder"
        self.refresh_inbox()
    
    def select_spam(self):
        "Select spam folder"
        self.refresh_inbox()
    
    def get_page_text(self):
        # document.getElementsByTagName("frame")[1].contentDocument.body.textContent
        # return self.driver.
        return self.driver.execute_script('return document.getElementsByTagName("frame")[1].contentDocument.body.textContent');
        
