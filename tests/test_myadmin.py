import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TestMyadminUI(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=r"/Users/armandosoaressousa/Desenvolvimento/UI/driver/chromedriver")
        self.driver.get("http://127.0.0.1:5000")
        usuario = self.driver.find_element_by_name("username")
        usuario.clear()
        usuario.send_keys("armando@armando")
        senha = self.driver.find_element_by_name("password")
        senha.clear()
        senha.send_keys("armando")
        senha.send_keys(Keys.RETURN)

    def test_carrega_membros(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/')
        membros_link = driver.find_element_by_link_text('View All Users')
        membros_link.click()

    def test_home(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/')
        home_link = driver.find_element_by_link_text('Home')
        home_link.click()

    def test_carrega_meus_repositorios(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/')
        meus_repositorios = driver.find_element_by_link_text('View All Repositories')
        meus_repositorios.click()

    def test_visualiza_repositorio(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/repositorio/listar')
        myadmin_link = driver.find_element_by_link_text('[Visualizar]')
        myadmin_link.click()

    def test_sair(self):
        driver = self.driver
        driver.get('http://127.0.0.1:5000/')
        sair_link = driver.find_element_by_link_text('Sair')
        sair_link.click()

    def tearDown(self):
        self.driver.close()