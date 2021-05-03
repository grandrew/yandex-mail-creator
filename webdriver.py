# from seleniumwire import webdriver

import random
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tbselenium.tbdriver import TorBrowserDriver
import time
import os
import os.path
import inspect

import tbselenium.common as cm
from tbselenium.utils import launch_tbb_tor_with_stem

options = {
    'proxy': {
        'http': 'socks5://localhost:9050', 
        'https': 'socks5://localhost:9050',
        'no_proxy': 'localhost,127.0.0.1' # excludes
    }
}

class WebDriver:

    def __init__(self, opts=None):
        self.opts = opts
        self.driver = webdriver.Chrome(
            os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/chromedriver',
            chrome_options=opts, seleniumwire_options=options)
        self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(30)
        self.driver.set_script_timeout(30)
        self.driver.set_window_size(375, 667)

    def wait_until_page_loaded(self):
        return WebDriverWait(self.driver, 20).until(lambda driver:
                                                    driver.execute_script('return document.readyState'))

    def wait_until_ajax_response(self):
        return WebDriverWait(self.driver, 20).until(lambda driver:
                                                    driver.execute_script(
                                                        'return !!window.jQuery && jQuery.active == 0'))

    def wait_until_page_url(self, url):
        return WebDriverWait(self.driver, 20).until(lambda driver:
                                                    driver.current_url.startswith(url))

    def wait_until_page_url_not(self, url):
        return WebDriverWait(self.driver, 20).until(lambda driver:
                                                    not driver.current_url.startswith(url))

    def wait_until_page_url_ends_with(self, url):
        return WebDriverWait(self.driver, 20).until(lambda driver:
                                                    driver.current_url.endswith(url))

    def send_slow_key(self, element=None, keys=None):
        for key in keys:
            element.send_keys(key)
            time.sleep(0.1)

    def wait_element(self, by=None, element=None):
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((by, element)))

    def get_element(self, by=None, element=None):
        return self.driver.find_element(by, element)

    def get_parent_node(self, by=None, element=None, n=1):
        element = self.get_element(by, element)
        repeated_str = ''
        for i in range(n):
            repeated_str = repeated_str + '.parentNode'
        script = 'return arguments[0]{};'.format(repeated_str)
        return self.driver.execute_script(script, element)


from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary




# Uncomment these if you need additional information for debugging
#import logging
#logging.basicConfig(level=logging.DEBUG)


class TorDriver(WebDriver):
    def __init__(self, opts=None):
        print("TORRR")
        self.opts = opts

        # The location of the Tor Browser bundle
        # Update this to match the location on your computer
        tbb_dir = os.path.expanduser("~/Downloads/tor-browser_en-US/")

        # Disable Tor Launcher to prevent it connecting the Tor Browser to Tor directly
        os.environ['TOR_SKIP_LAUNCH'] = '1'
        os.environ['TOR_TRANSPROXY'] = '1'

        # Set the Tor Browser binary and profile
        tb_binary = os.path.join(tbb_dir, 'Browser/firefox')
        tb_profile = os.path.join(tbb_dir, 'Browser/TorBrowser/Data/Browser/profile.default')
        binary = FirefoxBinary(os.path.join(tbb_dir, 'Browser/firefox'))
        profile = FirefoxProfile(tb_profile)

        # We need to disable HTTP Strict Transport Security (HSTS) in order to have
        #   seleniumwire between the browser and Tor. Otherwise, we will not be able
        #   to capture the requests and responses using seleniumwire.
        profile.set_preference("security.cert_pinning.enforcement_level", 0)
        profile.set_preference("network.stricttransportsecurity.preloadlist", False)

        # Tell Tor Button it is OK to use seleniumwire
        profile.set_preference("extensions.torbutton.local_tor_check", False)
        profile.set_preference("extensions.torbutton.use_nontor_proxy", True)

        # Required if you need JavaScript at all, otherwise JS stays disabled regardless
        #   of the Tor Browser's security slider value
        profile.set_preference("browser.startup.homepage_override.mstone", "68.8.0");

        # Configure seleniumwire to upstream traffic to Tor running on port 9050
        #   You might want to increase/decrease the timeout if you are trying
        #   to a load page that requires a lot of requests. It is in seconds.
        options = {
            'proxy': {
                'http': 'socks5h://127.0.0.1:9050',
                'https': 'socks5h://127.0.0.1:9050',
                'connection_timeout': 10
            }
        }

        self.driver = webdriver.Firefox(
            executable_path=
                os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/geckodriver',
                                firefox_profile=profile,
                                firefox_binary=binary,
                                # seleniumwire_options=options
                                )
        self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(30)
        self.driver.set_script_timeout(30)

def set_proxy(driver, http_addr='', http_port=0, ssl_addr='', ssl_port=0, socks_addr='', socks_port=0):

    driver.execute("SET_CONTEXT", {"context": "chrome"})

    try:
        driver.execute_script("""
          Services.prefs.setIntPref('network.proxy.type', 1);
          Services.prefs.setBoolPref('network.proxy.socks_remote_dns', true);
          Services.prefs.setCharPref("network.proxy.http", arguments[0]);
          Services.prefs.setIntPref("network.proxy.http_port", arguments[1]);
          Services.prefs.setCharPref("network.proxy.ssl", arguments[2]);
          Services.prefs.setIntPref("network.proxy.ssl_port", arguments[3]);
          Services.prefs.setCharPref('network.proxy.socks', arguments[4]);
          Services.prefs.setIntPref('network.proxy.socks_port', arguments[5]);
          """, http_addr, http_port, ssl_addr, ssl_port, socks_addr, socks_port)

    finally:
        driver.execute("SET_CONTEXT", {"context": "content"})

class TorDriver2(WebDriver):
    def __init__(self, opts):
        tbb_dir = os.path.expanduser("~/Downloads/tor-browser_en-US/")
        os.environ['TOR_SKIP_LAUNCH'] = '1'
        os.environ['TOR_TRANSPROXY'] = '1'
        tb_binary = os.path.join(tbb_dir, 'Browser/firefox')
        # tb_profile = os.path.join(tbb_dir, 'Browser/TorBrowser/Data/Browser/profile.default')
        tb_profile = os.path.join("profile"+str(int(time.time())))
        os.mkdir(tb_profile)
        binary = FirefoxBinary(os.path.join(tbb_dir, 'Browser/firefox'))
        profile = FirefoxProfile(tb_profile)

        ip='127.0.0.1'
        port = 9050 #of file  tor_port
        profile.set_preference('network.proxy.type', 1)
        profile.set_preference('network.proxy.socks', ip)
        profile.set_preference('network.proxy.socks_port', port)
        profile.set_preference('network.proxy.socks_version', 5)
        profile.set_preference('network.proxy.socks_remote_dns', True)
        profile.update_preferences()

        proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            "socksProxy": "127.0.0.1:9050"
            })
        profile.set_proxy(proxy)

        geckopath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/geckodriver'

        self.driver = webdriver.Firefox(
            executable_path=geckopath,
            firefox_profile=profile,
            firefox_binary=binary,
            proxy=proxy
            )
        
        set_proxy(self.driver, socks_addr="127.0.0.1", socks_port=9050)
        # self.driver.get("about:config");


        # self.driver.get('http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page')
        self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(30)
        self.driver.set_script_timeout(30)
        self.driver.set_window_size(375+random.randint(5,150), 667+random.randint(5,150))

class TorDriver3(WebDriver):
    def __init__(self, opts):
        tbb_dir = os.path.expanduser("~/Downloads/tor-browser_en-US/")
        os.environ['TOR_SKIP_LAUNCH'] = '1'
        os.environ['TOR_TRANSPROXY'] = '1'
        tb_binary = os.path.join(tbb_dir, 'Browser/firefox')
        # tb_profile = os.path.join(tbb_dir, 'Browser/TorBrowser/Data/Browser/profile.default')
        tb_profile = os.path.join("profile"+str(int(time.time())))
        os.mkdir(tb_profile)
        binary = FirefoxBinary(os.path.join(tbb_dir, 'Browser/firefox'))

        self.driver = TorBrowserDriver(tbb_dir,
            executable_path=
                os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/geckodriver',
            tor_cfg=cm.USE_STEM
        )
        
        # self.driver.get('http://zqktlwi4fecvo6ri.onion/wiki/index.php/Main_Page')
        self.driver.delete_all_cookies()
        self.driver.set_page_load_timeout(30)
        self.driver.set_script_timeout(30)