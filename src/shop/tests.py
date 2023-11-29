from django.test import TestCase

import time
import json
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service
from django.core.management import call_command
from selenium.webdriver.support import expected_conditions as EC
'''
class TestFull(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.driver = webdriver.Firefox()
        cls.driver.implicitly_wait(3)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        call_command('loaddata', 'populate.json')

    def test_full(self):
        self.driver.get(self.live_server_url)
        self.driver.set_window_size(1695, 1087)
        self.driver.find_element(By.LINK_TEXT, "Registrarse").click()
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("pepe@pepe.com")
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("1111")
        self.driver.find_element(By.ID, "full_name").clear()
        self.driver.find_element(By.ID, "full_name").click()
        self.driver.find_element(By.ID, "full_name").send_keys("pepito pepe pepón")
        self.driver.find_element(By.ID, "phone").clear()
        self.driver.find_element(By.ID, "phone").click()
        self.driver.find_element(By.ID, "phone").send_keys("123456789")
        self.driver.find_element(By.ID, "address").send_keys("Vivo en mi casa")
        self.driver.find_element(By.CSS_SELECTOR, ".submit > .btn").click()
        self.driver.find_element(By.LINK_TEXT, "Iniciar Sesión").click()
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("pepe@pepe.com")
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(Keys.ENTER)
        self.driver.find_element(By.ID, "password").send_keys("1111")
        self.driver.find_element(By.CSS_SELECTOR, ".submit > .btn").click()
        self.driver.find_element(By.CSS_SELECTOR, ".categoria-img > img").click()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(2) img").click()
        self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(3) img").click()
        self.driver.find_element(By.CSS_SELECTOR, ".categoria-img > img").click()
        self.driver.find_element(By.LINK_TEXT, "Más detalles").click()
        self.driver.find_element(By.CSS_SELECTOR, ".qtyminus").click()
        self.driver.find_element(By.CSS_SELECTOR, ".qtyminus").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".qtyminus")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, ".qtyminus").click()
        self.driver.find_element(By.CSS_SELECTOR, ".qtyminus").click()
        element = self.driver.find_element(By.CSS_SELECTOR, ".qtyminus")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.CSS_SELECTOR, ".qtyminus").click()
        self.driver.find_element(By.CSS_SELECTOR, ".qtyplus").click()
        self.driver.find_element(By.CSS_SELECTOR, ".round-black-btn").click()
        self.driver.find_element(By.ID, "quantityInputPart").click()
        self.driver.find_element(By.ID, "quantityInputPart").send_keys("3")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-refresh").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(2)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".navbar > a:nth-child(1) > img").click()
        self.driver.find_element(By.CSS_SELECTOR, ".item:nth-child(1) .col-sm-4:nth-child(3) .sin-estilo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-danger:nth-child(3)").click()
        self.driver.find_element(By.CSS_SELECTOR, ".navbar > a:nth-child(1) > img").click()
        self.driver.find_element(By.CSS_SELECTOR, ".item:nth-child(1) .col-sm-4:nth-child(2) .sin-estilo").click()
        self.driver.find_element(By.LINK_TEXT, "Continuar comprando").click()
        self.driver.find_element(By.CSS_SELECTOR, ".right").click()
        self.driver.find_element(By.CSS_SELECTOR, ".right").click()
        self.driver.find_element(By.CSS_SELECTOR, ".categoria-img > img").click()
        self.driver.find_element(By.CSS_SELECTOR, ".items-row:nth-child(2) > .col-sm-4:nth-child(3) .separator .hidden-sm").click()
        self.driver.find_element(By.CSS_SELECTOR, ".round-black-btn").click()
        self.driver.find_element(By.LINK_TEXT, "Finalizar").click()
        self.driver.find_element(By.ID, "payment_method").click()
        self.driver.find_element(By.CSS_SELECTOR, "#payment_method > option:nth-child(1)").click()
        self.driver.find_element(By.ID, "shipment").click()
        self.driver.find_element(By.CSS_SELECTOR, "#shipment > option:nth-child(1)").click()
        self.driver.find_element(By.NAME, "email").click()
        self.driver.find_element(By.NAME, "city").click()
        self.driver.find_element(By.NAME, "city").send_keys("Sevilla")
        self.driver.find_element(By.NAME, "postal_code").send_keys("41720")
        self.driver.find_element(By.CSS_SELECTOR, ".hidden-xs > strong").click()
        self.driver.find_element(By.CSS_SELECTOR, ".btn-primary").click()
        self.driver.find_element(By.CSS_SELECTOR, ".navbar > a:nth-child(1) > img").click()
        self.driver.find_element(By.LINK_TEXT, "Bienvenido, pepito pepe pepón").click()
        self.driver.find_element(By.CSS_SELECTOR, "#logoutForm > .sin-estilo").click()
        self.driver.find_element(By.CSS_SELECTOR, ".right").click()
        self.driver.find_element(By.CSS_SELECTOR, ".item:nth-child(2) .col-sm-4:nth-child(3) .sin-estilo").click()
        self.driver.find_element(By.ID, "quantityInputPart").click()
        self.driver.find_element(By.ID, "quantityInputPart").send_keys("200")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-refresh").click()
        self.driver.find_element(By.ID, "quantityInputPart").click()
        self.driver.find_element(By.ID, "quantityInputPart").send_keys("3")
        self.driver.find_element(By.CSS_SELECTOR, ".glyphicon-refresh").click()
        self.driver.find_element(By.CSS_SELECTOR, ".navbar > a:nth-child(1) > img").click()
        self.driver.find_element(By.CSS_SELECTOR, ".right").click()
        self.driver.find_element(By.CSS_SELECTOR, ".right").click()
        self.driver.find_element(By.CSS_SELECTOR, ".right").click()
        self.driver.find_element(By.CSS_SELECTOR, ".categoria-img > img").click()
        self.driver.find_element(By.LINK_TEXT, "Más detalles").click()
        self.driver.find_element(By.CSS_SELECTOR, ".round-black-btn").click()
        self.driver.find_element(By.LINK_TEXT, "Finalizar").click()
        self.driver.find_element(By.ID, "payment_method").click()
        dropdown = self.driver.find_element(By.ID, "payment_method")
        dropdown.find_element(By.XPATH, "//option[. = 'Tarjeta']").click()
        self.driver.find_element(By.CSS_SELECTOR, "#payment_method > option:nth-child(2)").click()
        self.driver.find_element(By.ID, "shipment").click()
        dropdown = self.driver.find_element(By.ID, "shipment")
        dropdown.find_element(By.XPATH, "//option[. = 'Envio a domicilio']").click()
        self.driver.find_element(By.CSS_SELECTOR, "#shipment > option:nth-child(2)").click()
        self.driver.find_element(By.NAME, "email").click()
        self.driver.find_element(By.NAME, "email").click()
        element = self.driver.find_element(By.NAME, "email")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.NAME, "email").click()
        self.driver.find_element(By.NAME, "email").click()
        element = self.driver.find_element(By.NAME, "email")
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.driver.find_element(By.NAME, "email").send_keys("guaje")
        self.driver.find_element(By.NAME, "email").send_keys(Keys.DOWN)
        self.driver.find_element(By.NAME, "email").send_keys(Keys.TAB)
        self.driver.find_element(By.NAME, "full_name").send_keys("Jose Antonio")
        self.driver.find_element(By.NAME, "phone").click()
        self.driver.find_element(By.NAME, "phone").send_keys("908980907")
        self.driver.find_element(By.NAME, "city").click()
        self.driver.find_element(By.NAME, "city").send_keys("LP")
        self.driver.find_element(By.NAME, "postal_code").send_keys("789120321")
        self.driver.find_element(By.NAME, "address").send_keys("xxxx")
        self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(9)").click()
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "email")))
        self.driver.find_element(By.ID, "email").clear()
        self.driver.find_element(By.ID, "email").click()
        self.driver.find_element(By.ID, "email").send_keys("sb-k43ebi28280380@personal.example.com")
        self.driver.find_element(By.ID, "btnNext").click()
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "password")))
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").click()
        self.driver.find_element(By.ID, "password").send_keys("nNU<<9Y%")
        self.driver.find_element(By.ID, "btnLogin").click()
        WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, "payment-submit-btn")))
        self.driver.find_element(By.ID, "payment-submit-btn").click()
'''
        
  

