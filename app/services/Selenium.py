from datetime import datetime
from matplotlib.pyplot import cla
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
import pdb

BC_ADRESS = "Mail or Wallet"
PASSWORD = "PASSWORD"

class Selenium(): 

    def __init__(self) -> None:
        self.chrome_service = fs.Service(executable_path='./chromedriver') 
        self.b = webdriver.Chrome(service=self.chrome_service)
        self.b.get('https://app.highlow.com/quick-demo?source=header-quick-demo-cta')
        self.s()
    
    def purchase(self, high_low_xxx):

        if high_low_xxx == "high":
            self.b.find_element(by=By.XPATH,value = "//div[text()='High']").click()
            self.s(0.5)
            self.b.find_element(by=By.XPATH,value = "//div[text()='今すぐ購入']").click()
            self.s(0.5)
            self.b.find_element(by=By.XPATH,value = "//div[text()='High']").click()
        
        elif high_low_xxx == "low":
            self.b.find_element(by=By.XPATH,value = "//div[text()='Low']").click()
            self.s(0.5)
            self.b.find_element(by=By.XPATH,value = "//div[text()='今すぐ購入']").click()
            self.s(0.5)
            self.b.find_element(by=By.XPATH,value = "//div[text()='Low']").click()

    @classmethod
    def l(cls,str):
        print("%s : %s"%(datetime.now().strftime("%Y/%m/%d %H:%M:%S"),str), flush=True)

    @staticmethod
    def s(t = 5):
        import time
        time.sleep(t)

    @staticmethod
    def x(str = ""):
        import traceback
        traceback.print_exc()
        if str != "":
            Selenium.l(str)

