# -*- coding:utf8 -*-

import os, sys, time, threading, random, datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from PIL import Image

sys.path.append("..")
from conf import PCEGGS_ACCOUNTS
from emailapi import emailApi

PATH = os.getcwd()

class PCeggs(object):
    def __init__(self, driver, msgManager):
        self.driver     = driver
        self.msgManager = msgManager

    def run(self):
        for account in PCEGGS_ACCOUNTS:
            user = account["user"]
            pwd = account["pwd"]
            self.__login(user, pwd)
            self.__sign()
            self.__flushcookie()

    def __login(self, user, pwd):
        url = "http://www.pceggs.com/nologin.aspx"
        self.driver.get(url)
        loginBtnLocator = (By.ID, "Login_Submit")
        try:
            WebDriverWait(self.driver, 10, 0.5).until(EC.element_to_be_clickable(loginBtnLocator))
        except TimeoutException:
            self.msgManager.sendMsg(u"PCeggs:无法定位到登录按钮！", "text")
        else:
            yzmElement = self.driver.find_element_by_id("valiCode")
            self.__sendYZM(yzmElement)
            yzm = self.__getYZM()
            self.driver.find_element_by_id("txt_UserName").send_keys(user)
            self.driver.find_element_by_id("txt_PWD").send_keys(pwd)
            self.driver.find_element_by_id("txt_VerifyCode").send_keys(yzm)
            self.driver.find_element_by_id("Login_Submit").click()

    def __sign(self):
        pass

    def __sendYZM(self, yzmElement):
        self.driver.save_screenshot("xx.png")
        left = int(yzmElement.location["x"])
        top = int(yzmElement.location["y"])
        right = int(yzmElement.location["x"]+yzmElement.size["width"])
        bottom = int(yzmElement.location["y"]+yzmElement.size["height"])
        im = Image.open("xx.png")
        im = im.crop((left, top, right, bottom))
        im.save("yzm.png")
        self.msgManager.sendMsg(os.path.join(PATH, "yzm.png"), "image")
        self.msgManager.sendMsg(u"PCeggs:输入验证码,格式:@+验证码", "text")

    def __getYZM(self):
        while True:
            time.sleep(8)
            yzm = self.msgManager.getYZM()
            if yzm in [None,""]:
                yzm = self.emailApi.recvEmail()
            if yzm:
                print yzm
                break
        self.msgManager.sendMsg(u"PCeggs:输入的验证码: %s" % yzm, "text")
        return yzm

    def __flushcookie(self):
        pass

