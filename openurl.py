import urllib2
import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class openurl(object):
    firefox_profile = None
    browser = None

    def __init__(self):
        firefox_profile = webdriver.FirefoxProfile()

        firefox_profile.set_preference("network.http.pipelining", True)
        firefox_profile.set_preference("network.http.proxy.pipelining", True)
        firefox_profile.set_preference("network.http.pipelining.maxrequests", 8)
        firefox_profile.set_preference("content.notify.interval", 500000)
        firefox_profile.set_preference("content.notify.ontimer", True)
        firefox_profile.set_preference("content.switch.threshold", 250000)
        firefox_profile.set_preference("browser.cache.memory.capacity", 65536) # Increase the cache capacity.
        firefox_profile.set_preference("browser.startup.homepage", "about:blank")
        firefox_profile.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
        firefox_profile.set_preference("browser.pocket.enabled", False) # Duck pocket too!
        firefox_profile.set_preference("loop.enabled", False)
        firefox_profile.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
        firefox_profile.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
        firefox_profile.set_preference("browser.display.use_document_colors", False) # Don't show document colors.
        firefox_profile.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
        firefox_profile.set_preference("browser.display.use_system_colors", True) # Use system colors.
        firefox_profile.set_preference("browser.formfill.enable", False) # Autofill on forms disabled.
        firefox_profile.set_preference("browser.helperApps.deleteTempFileOnExit", True) # Delete temprorary files.
        firefox_profile.set_preference("browser.shell.checkDefaultBrowser", False)
        firefox_profile.set_preference("browser.startup.homepage", "about:blank")
        firefox_profile.set_preference("browser.startup.page", 0) # blank
        firefox_profile.set_preference("browser.tabs.forceHide", True) # Disable tabs, We won't need that.
        firefox_profile.set_preference("browser.urlbar.autoFill", False) # Disable autofill on URL bar.
        firefox_profile.set_preference("browser.urlbar.autocomplete.enabled", False) # Disable autocomplete on URL bar.
        firefox_profile.set_preference("browser.urlbar.showPopup", False) # Disable list of URLs when typing on URL bar.
        firefox_profile.set_preference("browser.urlbar.showSearch", False) # Disable search bar.
        firefox_profile.set_preference("extensions.checkCompatibility", False) # Addon update disabled
        firefox_profile.set_preference("extensions.checkUpdateSecurity", False)
        firefox_profile.set_preference("extensions.update.autoUpdateEnabled", False)
        firefox_profile.set_preference("extensions.update.enabled", False)
        firefox_profile.set_preference("general.startup.browser", False)
        firefox_profile.set_preference("plugin.default_plugin_disabled", False)
        firefox_profile.set_preference("permissions.default.image", 2) # Image load disabled again
        #firefox_profile.set_preference('permissions.default.image', 2)
        #firefox_profile.set_preference("network.cookie.cookieBehavior", 2) # disable cookie
        firefox_profile.set_preference('permissions.default.stylesheet', 2) ## Disable CSS
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')  ## Disable Flash
        
        # set headleess | invisble mode
        options = Options()
        options.set_headless(headless=True)

        self.browser = webdriver.Firefox(firefox_options=options, executable_path = 'geckodriver.exe', firefox_profile=firefox_profile)
        #self.browser = webdriver.Firefox(executable_path = 'geckodriver.exe', firefox_profile=firefox_profile)


    def get(self, url):
        self.browser.get(url)
        return self.browser.page_source

    def simple_get1(url):
        response = requests.get(url)
        return response.text

    def simple_get2(url):
        response = urllib2.urlopen(url)
        return response.read()


    def close(self):
         self.browser.quit()
