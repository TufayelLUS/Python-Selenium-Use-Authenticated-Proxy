from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

# to change type of proxy, please change scheme: "https" into http,socks5,https
PROXY_HOST = 'host'  # proxy, without http/https
PROXY_PORT = 1251 # port, number
PROXY_USER = 'username'
PROXY_PASS = 'password'

def createBrowser(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS):

    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "https",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    chrome_options = Options()
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #chrome_options.add_experimental_option("prefs", prefs)
    #chrome_options.add_argument("--headless") #uncomment to disable opening of browser window
    #chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36")
    #chrome_options.add_argument("--load-extension=" + os.getcwd() + "/setupvpn")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--log-level=3")
    pluginfile = 'proxy_auth_plugin.zip'
    with zipfile.ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    chrome_options.add_extension(pluginfile)
    #chrome_options.add_argument("--proxy-server=https://qiwf-832ad0.sheep-managing.org:1251")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    return driver


if __name__ == "__main__":
    driver = createBrowser(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)
    driver.get("http://api.ipify.org")
