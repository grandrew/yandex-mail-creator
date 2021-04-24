import inspect
import os
import random

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import base64
import requests
# from webdriver import TorDriver, TorDriver2, WebDriver
from webdriver import TorDriver2 as WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from smsactivateru import Sms, SmsTypes, SmsService, GetBalance, GetFreeSlots, GetNumber 

import threading
import functools

class SmsYandex(WebDriver):

    def __init__(self, account=None, api_key=None):
        opts = Options()
        opts.add_experimental_option('prefs', {'intl.accept_languages': 'tr-TR,tr;q=0.8,en-US;q=0.6,en;q=0.4'})
        opts.add_argument(
            '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
        opts.add_argument(
            '--proxy-server="socks5://localhost:9050"')
        WebDriver.__init__(self, opts)
        self.registerPage = 'http://mail.yandex.com/'
        # self.registerPage = 'https://myip.ru/'
        self.apiKey = api_key
        self.account = account
        self.id = None
        self.interface = "full"

    def create_account(self):
        # self.driver.set_window_size(1024, 768)
        ok = False
        while not ok:
            self.driver.get(self.registerPage)
            # time.sleep(2)

            # actions = ActionChains(self.driver)
            # actions.moveByOffset(382, 482).click().build().perform()
            for i in range(100):
                try:
                    self.driver.execute_script("return document.querySelector('#index-page-container > div > div.HeadBanner.with-her > div > div > div.HeadBanner-ButtonsWrapper > a.control.button2.button2_view_classic.button2_size_mail-big.button2_theme_mail-action.button2_type_link.HeadBanner-Button.with-shadow').click();");
                    ok = True
                    break
                except:
                    time.sleep(0.05)
                    # self.driver.execute_script("return document.querySelector('#index-page-container > div > div.HeadBanner.with-her > div > div > div.HeadBanner-ButtonsWrapper > a.control.button2.button2_view_classic.button2_size_mail-big.button2_theme_mail-action.button2_type_link.HeadBanner-Button.with-shadow').click();");
        if not ok:
            self.driver.quit()
            raise Exception("Could not continue")
        time.sleep(1)
        if 1:
        # try:
            # for i in range(500):
            #     try:
            #         self.get_element(By.CSS_SELECTOR, "#index-page-container > div > div.HeadBanner.with-her > div > div > div.HeadBanner-ButtonsWrapper > a.control.button2.button2_view_classic.button2_size_mail-big.button2_theme_mail-action.button2_type_link.HeadBanner-Button.with-shadow").click()
            #         break
            #     except:
            #         pass
            # self.wait_until_page_loaded()
            # try:
                # self.get_element(By.CSS_SELECTOR, "#index-page-container > div > div.HeadBanner.with-her > div > div > div.HeadBanner-ButtonsWrapper > a.control.button2.button2_view_classic.button2_size_mail-big.button2_theme_mail-action.button2_type_link.HeadBanner-Button.with-shadow").click()
            # except:
                # pass
            # time.sleep(200)
            # for i in range(100):
                # try:
                    # self.get_element(By.CSS_SELECTOR, "#index-page-container > div > div.HeadBanner.with-her > div > div > div.HeadBanner-ButtonsWrapper > a.control.button2.button2_view_classic.button2_size_mail-big.button2_theme_mail-action.button2_type_link.HeadBanner-Button.with-shadow").click()
                # except:
                    # self.get_element(By.CSS_SELECTOR, "#index-page-container > div > div.HeadBanner.with-him > div > div > div.HeadBanner-ButtonsWrapper > a.control.button2.button2_view_classic.button2_size_mail-big.button2_theme_mail-action.button2_type_link.HeadBanner-Button.with-shadow").click()
                    # print("ERRRRRRR")
                    # time.sleep(1)
            self.wait_until_page_loaded()
            time.sleep(2)

            self.wait_element(By.CSS_SELECTOR, '#firstname')

            first_name_element = self.get_element(By.ID, 'firstname')
            last_name_element = self.get_element(By.ID, 'lastname')
            login_element = self.get_element(By.ID, 'login')

            self.send_slow_key(first_name_element, self.account.firstName)

            self.send_slow_key(last_name_element, self.account.lastName)
            self.wait_until_ajax_response()

            self.account.mail += ''.join([str(random.randint(0,9)), str(random.randint(0,9))])
            self.send_slow_key(login_element, self.account.mail)
            self.wait_until_ajax_response()

            mail_retry_count = 0
            parent = self.get_parent_node(By.ID, 'login', 2)

            while 'field__error' in parent.get_attribute('class') and mail_retry_count < 3:
                login_element.clear()
                # self.account.mail = self.account.mail + ''.join([str(random.randint(0,9)), str(random.randint(0,9))])
                self.send_slow_key(login_element, ''.join([str(random.randint(0,9)), str(random.randint(0,9))]))
                self.wait_until_ajax_response()
                time.sleep(1)
                mail_retry_count += 1
                if mail_retry_count == 3:
                    self.driver.quit()

            password_element = self.get_element(By.ID, 'password')
            self.send_slow_key(password_element, self.account.password)
            self.wait_until_ajax_response()

            password_confirm_element = self.get_element(By.ID, 'password_confirm')
            self.send_slow_key(password_confirm_element, self.account.password)
            self.wait_until_ajax_response()

            self.registered_stats = ('Email adresi {}@yandex.com ve sifre {} olarak belirlendi'.format(
                self.driver.find_element_by_id('login').get_attribute('value'), self.account.password))

            # time.sleep(1000)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

            # wait for javascript
            # TODO: confirm number .Button2_view_pseudo  .Button2_view_pseudo
            # wait for javascript
            # button.Button2:nth-child(1)


            self.fill_other_fields()

        # finally:
        #     print(self.registered_stats)
        #     # self.driver.quit()
        #     pass

    def decode_capthca(self):
        captcha_element = self.get_element(By.CSS_SELECTOR, '.captcha__image')
        captcha_url = captcha_element.get_attribute('src')
        print('Capthca cozuluyor')
        b64_captcha = base64.b64encode(requests.get(captcha_url).content)
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

        captcha_element = self.get_element(By.ID, 'captcha')
        captcha_element.clear()
        self.send_slow_key(captcha_element, text)

    def confirm_sms(self):
        phone_num_element = self.get_element(By.ID, 'phone')
        wrapper = Sms(open("smsreg.apikey").read())
        # getting balance
        balance = GetBalance().request(wrapper)
        # show balance
        print('На счету {} руб.'.format(balance))
        # getting free slots (count available phone numbers for each services)
        available_phones = GetFreeSlots(
            country=SmsTypes.Country.CA,
            # operator=SmsTypes.Operator.TELE2
        ).request(wrapper)
        # show for vk.com, whatsapp and youla.io)
        # print('vk.com: {} номеров'.format(available_phones.VkCom.count))
        # print('whatsapp: {} номеров'.format(available_phones.Whatsapp.count))
        # print('youla.io: {} номеров'.format(available_phones.Youla.count))
        print('yandex: {} номеров'.format(available_phones.Yandex.count))
        activation = GetNumber(
            service=SmsService().Yandex,
            country=SmsTypes.Country.CA,
            # operator=SmsTypes.Operator.Beeline
        ).request(wrapper)

        # show activation id and phone for reception sms
        print('id: {} phone: {}'.format(str(activation.id), str(activation.phone_number)))
        self.send_slow_key(phone_num_element, "+"+activation.phone_number)
        self.wait_until_ajax_response()
        time.sleep(2)
        try:
            confirm_sms_button = self.get_element(By.CSS_SELECTOR, '.Button2_view_pseudo')  # phone confirm click
            confirm_sms_button.click()
        except:
            pass
        time.sleep(1)
        try:
            confirm_sms_button = self.get_element(By.CSS_SELECTOR, '.Button2_view_pseudo')  # phone confirm click
            confirm_sms_button.click()
        except:
            pass
        time.sleep(1)
        try:
            confirm_registration_element = self.get_element(By.CSS_SELECTOR, 'button[type="submit"]')
            confirm_registration_element.click()
        except:
            pass

        # GET CODE HERE

        activation.was_sent()
        # .request(wrapper)
        code = activation.wait_code(wrapper=wrapper)

        phone_code_element = self.get_element(By.ID, 'phoneCode')
        self.send_slow_key(phone_code_element, code)
        self.wait_until_ajax_response()



    def fill_other_fields(self):
        # self.decode_capthca()
        self.confirm_sms()
        self.wait_element(By.CSS_SELECTOR, 'button[type="submit"]')
        try:
            confirm_registration_element = self.get_element(By.CSS_SELECTOR, 'button[type="submit"]')
            confirm_registration_element.click()
        except:
            self.driver.execute_script("return document.querySelector('button[type=\"submit\"]').click();")
        self.wait_until_ajax_response()
        time.sleep(1)

        for i in range(5):
            try:
                if self.get_element(By.CSS_SELECTOR, '.form__popup-error') is not None:
                    print('Hatali captcha.')
                    text_result = requests.get(
                        "http://2captcha.com/res.php?key=" + self.apiKey + "&action=reportbad&id=" + self.id).text
                    if text_result == 'OK_REPORT_RECORDED':
                        print('Hatali captcha rapor edildi')
                    time.sleep(0.5)
                    self.fill_other_fields()
                    return
            except NoSuchElementException:
                break
        if self.get_element(By.CLASS_NAME, 'eula-popup__show') is None:
            pass
        else:
            try:
                self.get_element(By.CSS_SELECTOR,
                             "#root > div > div.grid > div > main > div > div > div > form > div.form__submit > div > div.eula-popup > div > button").click()
                self.get_element(By.CSS_SELECTOR,
                             '#root > div > div.grid > div > main > div > div > div > form > div.form__submit > div > div.eula-popup > button').click()
            except:
                print("Could not click EULA(ok, continue)")
                time.sleep(5)
        # #root > div > div:nth-child(1) > div.main-container > main > div > div > div > div.registration__avatar-buttons > span > a
        try:
            self.get_element(By.CSS_SELECTOR, '#root > div > div:nth-child(1) > div.main-container > main > div > div > div > div.registration__avatar-buttons > span > a').click()
        except:
            pass

        self.wait_until_page_loaded()
        time.sleep(2)

        try:
            self.get_element(By.CSS_SELECTOR, '#root > div > div:nth-child(1) > div.main-container > main > div > div > div > div.registration__avatar-buttons > span > a').click()
        except:
            pass

        try:
            form_button_enter = self.get_element(By.CSS_SELECTOR, '.new-hr-auth-Form_Button-enter')
            if form_button_enter is not None:
                form_button_enter.click()
                self.wait_until_page_loaded()

                new_login_element = self.get_element(By.CSS_SELECTOR, 'input[name="login"]')
                self.send_slow_key(new_login_element, self.account.mail)

                new_password_element = self.get_element(By.CSS_SELECTOR, 'input[name="passwd"]')
                self.send_slow_key(new_password_element, self.account.password)

                password_button_element = self.get_element(By.CSS_SELECTOR, '.passport-Button')
                password_button_element.click()
        except NoSuchElementException:
            pass

        self.wait_until_page_url('https://mail.yandex.com/?uid=')
        self.email_addr = self.account.mail + '@yandex.com' 
        print('001 Yandex hesabi basariyla olusturuldu')

        # try:
        #     self.wait_element(By.CSS_SELECTOR, '.js-get-mobile-app-link-skip')
        #     self.get_element(By.CSS_SELECTOR, '.js-get-mobile-app-link-skip').click()
        #     time.sleep(1)
        #     self.get_element(By.CSS_SELECTOR, '.mail-WelcomeWizard-ThemeStep-Buttons-Link').click()
        #     time.sleep(1)
        #     self.get_element(By.CSS_SELECTOR, '.js-go-to-next-step').click()
        #     time.sleep(2)
        # except:
        #     pass
        print('Yandex hesabi basariyla olusturuldu')
        file_path = os.path.dirname(
            os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/yandexaccounts.txt'
        with open(file_path, 'a') as file:
            file.write(self.account.mail + '@yandex.com:' + self.account.password + '\n')
    
    def switch_to_light(self):
        if self.interface == "full":
            self.get_element(By.CSS_SELECTOR, '.mail-App-Footer-Item_lite > a:nth-child(1)').click()
            self.interface = "light"
            self.wait_until_page_loaded()
            time.sleep(5)
    
    def refresh_inbox(self):
        "Refresh the inboxes. Don't forget to add delay to wait for reload"

        self.switch_to_light()
        self.get_element(By.CSS_SELECTOR, '.b-folders > div:nth-child(1) > span:nth-child(1) > span:nth-child(2) > a:nth-child(1)').click()
        self.wait_until_page_loaded()
    
    def select_inbox(self):
        "Select inbox folder"
        self.switch_to_light()
        # self.get_element(By.CSS_SELECTOR, 'a.ns-view-folder:nth-child(1)').click()
        try:
            self.get_element(By.CSS_SELECTOR, '.b-folders > div:nth-child(1) > span:nth-child(1) > span:nth-child(2) > a:nth-child(1)').click()
        except:
            self.get_element(By.CSS_SELECTOR, 'body > div.b-page > div.b-layout > div.b-layout__left > div > div:nth-child(1) > span.b-folders__folder.b-folders__folder_unread.b-folders__folder_current > span.b-folders__folder__name > a').click()
        self.wait_until_page_loaded()
    
    def select_spam(self):
        "Select spam folder"
        self.switch_to_light()
        # self.get_element(By.CSS_SELECTOR, 'a.ns-view-folder:nth-child(4)').click()
        try:
            self.get_element(By.CSS_SELECTOR, '.b-folders > div:nth-child(1) > span:nth-child(4) > span:nth-child(2) > a:nth-child(1)').click()
        except:
            self.get_element(By.CSS_SELECTOR, 'body > div.b-page > div.b-layout > div.b-layout__left > div > div:nth-child(1) > span:nth-child(4) > span > a').click()
        self.wait_until_page_loaded()
    
    def get_page_text(self):
        self.switch_to_light()
        el = self.driver.find_element_by_id('main')
        return el.text
        
