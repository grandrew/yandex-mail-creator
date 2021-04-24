import inspect
import os
import random

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import base64
import requests
from webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains


class Rambler(WebDriver):

    def __init__(self, account=None, api_key=None):
        opts = Options()
        opts.add_experimental_option('prefs', {'intl.accept_languages': 'tr-TR,tr;q=0.8,en-US;q=0.6,en;q=0.4'})
        opts.add_argument(
            '--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36')
        opts.add_argument(
            '--proxy-server="socks5://localhost:9050"')
        WebDriver.__init__(self, opts)
        self.registerPage = 'https://mail.rambler.ru/?utm_source=head&utm_campaign=self_promo&utm_medium=header&utm_content=mail' 
        self.apiKey = api_key
        self.account = account
        self.id = None
        self.interface = "full"


    def solve_captcha(self):
        self.driver.switch_to_default_content()
        # self.driver.switch_to_frame("0.0")
        gkey = self.driver.execute_script('return (new URLSearchParams(document.getElementsByTagName("iframe")[0].src)).get("k")')
        # gkey = self.driver.find_element_by_id("recaptcha").get_attribute("data-sitekey")
        print("RECAPTCHA:", gkey)
        r = requests.get('http://2captcha.com/in.php?key=206318f3ef77f0118eae3c1628f3c1aa&method=userrecaptcha&googlekey=%s&pageurl=https://burghquayregistrationoffice.inis.gov.ie/Website/AMSREG/AMSRegWeb.nsf/AppSelect?OpenForm' % gkey)
        res = r.text
        print("2cpt", res)
        try:
            rk = res.split("|")[1]
        except:
            rk = "12345"
        print("rk", rk)
        time.sleep(5)
        capRes = "CAPCHA_NOT_READY"
        i = 0
        while capRes == "CAPCHA_NOT_READY":
            print(capRes)
            r = requests.get("http://2captcha.com/res.php?key=206318f3ef77f0118eae3c1628f3c1aa&action=get&id=%s" % rk)
            capRes = r.text
            if capRes == "ERROR_WRONG_CAPTCHA_ID": raise BaseException("ERROR_WRONG_CAPTCHA_ID")
            time.sleep(2)
            i+=1
            if i > 60:
                raise BaseException("Captcha timeout")
        capRes = capRes.split("|")[1]
        print(capRes)
        self.driver.execute_script('document.getElementById("g-recaptcha-response").innerHTML="%s";' % capRes)

    def create_account(self):
        # self.driver.set_window_size(1024, 768)

        try:
            self.driver.get(self.registerPage)
            self.wait_until_page_loaded()
            time.sleep(2)
            # self.driver.switch_to_frame("login")
            self.driver.switch_to_frame("0")
            # Click register
            self.get_element(By.CSS_SELECTOR, '.footer-0-3-53 > a:nth-child(1)').click()
            self.wait_until_ajax_response()
            login_element = self.get_element(By.CSS_SELECTOR, '#login')
            self.send_slow_key(login_element, self.account.mail)
            # password

            password_element = self.get_element(By.CSS_SELECTOR, '#newPassword')
            self.send_slow_key(password_element, self.account.password)

            password_confirm_element = self.get_element(By.CSS_SELECTOR, '#confirmPassword')
            self.send_slow_key(password_confirm_element, self.account.password)

            # question

            self.get_element(By.CSS_SELECTOR, '#question').click()
            self.get_element(By.CSS_SELECTOR, 'div.rui-MenuItem-root:nth-child(1)').click()

            # type in answer

            index = "107234"
            answer_elem = self.get_element(By.CSS_SELECTOR, '#answer')
            self.send_slow_key(answer_elem, index)

            self.solve_captcha()

            # TODO: run callback to enable button!

            # Now click "next"
            self.get_element(By.CSS_SELECTOR, '.rui-Button-button').click()



            first_name_element = self.get_element(By.CSS_SELECTOR, '#firstname')
            last_name_element = self.get_element(By.CSS_SELECTOR, '#lastname')

            self.send_slow_key(first_name_element, self.account.firstName)
            self.send_slow_key(last_name_element, self.account.lastName)


            # Gender
            self.get_element(By.CSS_SELECTOR, '#gender').click()
            self.get_element(By.CSS_SELECTOR, 'div.rui-MenuItem-root:nth-child(1)').click()

            # birthday
            self.get_element(By.CSS_SELECTOR, '#birthday').click()
            self.get_element(By.CSS_SELECTOR, 'div.rui-MenuItem-root:nth-child(2)').click()

            # month
            self.get_element(By.CSS_SELECTOR, 'div.rui-Select-root:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)').click()
            self.get_element(By.CSS_SELECTOR, 'div.rui-MenuItem-root:nth-child(3)').click()

            # yesr
            self.get_element(By.CSS_SELECTOR, 'div.rui-Select-root:nth-child(3) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)').click()
            self.get_element(By.CSS_SELECTOR, 'div.rui-MenuItem-root:nth-child(22)').click()

            # City
            city = self.get_element(By.CSS_SELECTOR, '#geoid')
            self.send_slow_key(city, "Moscow")
            time.sleep(2)
            self.wait_until_ajax_response()
            self.get_element(By.CSS_SELECTOR, 'div.rui-MenuItem-root:nth-child(3)').click()









            self.wait_until_ajax_response()
            time.sleep(1)

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
            try:
                self.get_element(By.CSS_SELECTOR, '.link_has-no-phone').click()
            except:
                pass
            self.wait_until_ajax_response()
            time.sleep(1)

            self.registered_stats = ('Email adresi {}@yandex.com ve sifre {} olarak belirlendi'.format(
                self.driver.find_element_by_id('login').get_attribute('value'), self.account.password))

            hint_answer = self.get_element(By.ID, 'hint_answer')
            if hint_answer.get_attribute('value').strip() == '':
                self.send_slow_key(hint_answer, self.account.firstName + ' ' + self.account.lastName)

            # time.sleep(1000)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            self.fill_other_fields()

        finally:
            print(self.registered_stats)
            # self.driver.quit()
            pass

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

    def fill_other_fields(self):
        self.decode_capthca()
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
        
