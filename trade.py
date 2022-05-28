from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import sys

class Trade:
    def __init__(self, profile=None, visible=True, size=None, check=5):
        self.funds = {}
        options_string=""
        if profile is not None:
            options_string=options_string + "user-data-dir=/home/arya/.config/google-chrome/Default"
        options = webdriver.ChromeOptions() 
        options.add_argument(options_string)
        if not visible:
            options.add_argument("--headless")
        if size is not None:
            options.add_argument("--window-size="+str(size).strip("()"))
        self.driver = webdriver.Chrome(options=options)
        self.actions = ActionChains(self.driver)
        self.driver.get("https://wazirx.com/exchange")
        self.wait = WebDriverWait(self.driver, 10)
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'buy')))
        self.get_funds()
    def find_symbol(self,symbol):
        search = self.driver.find_element_by_class_name('currency-search')
        search.click()
        search.clear()
        search.send_keys(symbol)
        ticker = self.driver.find_element_by_class_name('ticker-item').find_element_by_xpath("//a[@href='/exchange/"+symbol+"-INR']")
        ticker.click()
    def buy(self, symbol, price, amount, stop_price=False):
        minimum = 100
        # if self.funds["INR"] < amount or amount < minimum:
        #     return
        self.find_symbol(symbol)
        self.driver.find_element_by_css_selector('div.buy').click()
        form = self.driver.find_element_by_xpath("//form")
        atprice = form.find_element_by_xpath(".//span[. = 'AT PRICE']/../../input")
        totalinr = form.find_element_by_xpath(".//span[. = 'Total']/../../input")
        button = form.find_element_by_xpath(".//button[@type='submit']")
        if stop_price:
            totalinr = form.find_element_by_xpath(".//span[. = 'Total']/../../input")
        else:
            pass
        atprice.clear()
        atprice.send_keys(Keys.BACKSPACE*15)
        atprice.send_keys(str(price))
        totalinr.clear()
        totalinr.send_keys(Keys.BACKSPACE*15)
        if isinstance(amount, int) or amount.isdigit():
            value = str(amount)
        else:
            value = str(self.funds["INR"]*0.01*float(amount[:-1]))
        totalinr.send_keys(value)
        button.click()
        while self.driver.find_element_by_xpath('//nav/following-sibling::div').text == "":
            time.sleep(1)
        error = self.driver.find_element_by_xpath('//nav/following-sibling::div').text
        print(error)
        self.funds["INR"] = self.funds["INR"] - value
            
    def sell(self, symbol, price, amount, stop_price=False):
        minimum = 100
        # if self.funds["INR"] < amount or amount < minimum:
        #     return
        self.find_symbol(symbol)
        self.driver.find_element_by_css_selector('div.sell').click()
        form = self.driver.find_element_by_xpath("//form")
        atprice = form.find_element_by_xpath(".//span[. = 'AT PRICE']/../../input")
        totalinr = form.find_element_by_xpath(".//span[. = 'Total']/../../input")
        button = form.find_element_by_xpath(".//button[@type='submit']")
        if stop_price:
            totalinr = form.find_element_by_xpath(".//span[. = 'Total']/../../input")
        else:
            pass
        atprice.clear()
        atprice.send_keys(Keys.BACKSPACE*15)
        atprice.send_keys(str(price))
        totalinr.clear()
        totalinr.send_keys(Keys.BACKSPACE*15)
        if isinstance(amount, int) or amount.isdigit():
            totalinr.send_keys(str(amount))
        else:
            totalinr.send_keys(str(self.funds["INR"]*0.01*float(amount[:-1])))
        button.click()
        while self.driver.find_element_by_xpath('//nav/following-sibling::div').text == "":
            time.sleep(1)
        error = self.driver.find_element_by_xpath('//nav/following-sibling::div').text
        print(error)
        self.get_funds()
    def get_funds(self):
        self.funds = {}
        self.actions.move_to_element(self.driver.find_element_by_xpath("//a[@href='/funds']")).perform()
        portfolio = False
        for i in self.driver.find_element_by_id("popover").text.split('\n'):
            if any(map(str.isdigit, i)):
                print(i)
                if i[0] == "₹":
                    if portfolio:
                        self.funds["INR"] = float(i[1:].replace(',', ""))
                    else:
                        self.funds["Total"] = float(i[1:].replace(',', ""))
                        portfolio = True
                        
                else:
                    ii = i.split()
                    self.funds[ii[1]] = float(ii[0].replace(',', ""))
        
if __name__ == '__main__':
    trade = Trade(profile='/home/arya/.config/google-chrome')
    while True:
        try:
            eval(input("> "))
        except Exception as e:
            if e is KeyboardInterrupt:
                sys.exit()
            else:
                raise
