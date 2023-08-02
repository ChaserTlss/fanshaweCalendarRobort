from selenium import webdriver
from selenium.webdriver.common.by import By
import sys

class FanshaweCalendar(list):
    def __init__(self, titles, items):
        li = [ dict(zip(titles, item)) for item in items]
        super().__init__(li)

    def deley(function):
        def wrapper(*args, **kwargs):
            import time
            ret = function(*args, **kwargs)
            time.sleep(5)
            return ret
        return wrapper

    @staticmethod
    @deley
    def clickHrefFWA(driver, text):
        hreflist = driver.find_elements(By.TAG_NAME, "a")
        for href in hreflist:
            if href.text == text:
                href.click()
                return True
        print(f"Warrning: {text} not found")
        return False

    @staticmethod
    @deley
    def getFWA(url):
        try:
            driver = webdriver.Firefox()
            driver.get(url)
            return driver
        except:
            print("Warrning: Firefox driver not found")

        try:
            driver = webdriver.Chrome()
            driver.get(url)
            return driver
        except:
            print("Warrning: Chrome driver not found")

        try:
            driver = webdriver.Edge()
            driver.get(url)
            return driver
        except:
            print("Warrning: Edge driver not found")

        try:
            driver = webdriver.safari()
            driver.get(url)
            return driver
        except:
            print("Warrning: Safari driver not found")

        raise Exception("No driver found")

    @staticmethod
    @deley
    def loginFWA(driver, username, password):
        try:
            form = driver.find_element(By.TAG_NAME, "form")
            form.find_element(By.NAME, "USER.NAME").send_keys(username)
            form.find_element(By.NAME, "CURR.PWD").send_keys(password)
            form.submit()
            return True
        except:
            print("Warrning: Login failed")
            return False

    @staticmethod
    @deley
    def selectSemesterFWA(driver, semester):
        try:
            form = driver.find_element(By.TAG_NAME, "form")
            from selenium.webdriver.support.ui import Select
            select = Select(form.find_element(By.NAME, "VAR4"))
            select.select_by_value(semester)
            form.submit()
            return True
        except e:
            print("Warrning: Semester not found")
            print(e)
            return False

    @classmethod
    def getCalendarFromFWA(cls, username, password):
        URL = 'https://webadvisor.fanshawec.ca/'
        driver = cls.getFWA(URL)
        cls.clickHrefFWA(driver, "Log Out")
        cls.clickHrefFWA(driver, "Log In")
        cls.loginFWA(driver, username, password)
        cls.clickHrefFWA(driver, "Students")
        cls.clickHrefFWA(driver, "Class Schedule List")
        cls.selectSemesterFWA(driver, "23F")
        #get trs
        trs = driver.find_elements(By.TAG_NAME, "tbody")[-1].find_elements(By.TAG_NAME, "tr")
        #get titles
        titles = [th.text for th in trs[0].find_elements(By.TAG_NAME, "th") if th.text != ""]
        #get items
        items = [[td.text for td in tr.find_elements(By.TAG_NAME, "td") if td.text != ""] for tr in trs[1:]]
        driver.close()

        return cls(titles, items)



if __name__ == "__main__":
    d = FanshaweCalendar.getCalendarFromFWA(sys.argv[1], sys.argv[2])
    for x in d:
        print(x)


