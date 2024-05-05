from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import os

#works with a local rvc server https://github.com/Mangio621/Mangio-RVC-Fork.git

class Cover:
    
    def __init__(self, outputpath=".\\aicover\\audio"):
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True) # to keep  tabs open
        self.driver = webdriver.Chrome(options=chrome_options)

        self.models = {}
        self.update_models()
        self.driver.maximize_window()
        self.driver.get('http://localhost:7897/')
        sleep(2)
        self.outputpath = outputpath
    
    def WriteToField(self,id, tag, keys=None):
        """Write to any field having id-tag structure"""
        
        element = self.driver.find_element(By.ID, id)
        element = element.find_element(By.TAG_NAME, tag)
        element.clear()
        element.send_keys(keys)

    def separate(self, path):
        """Separate vocal and music"""
        
        mode = self.driver.find_element(By.XPATH, "//*[contains(text(), 'Vocals/Accompaniment Separation & Reverberation Removal')]")
        mode.click()
        # Audio to convert
        self.WriteToField("component-82","textarea", f"{path}\\queue")
        # Model
        self.WriteToField("component-86","input","HP3_all_vocals")
        self.driver.find_element(By.ID, "component-86").find_element(By.CLASS_NAME, "svelte-qgtjkt").click()
        # Output
        self.WriteToField("component-88","textarea",self.outputpath)
        self.WriteToField("component-89","textarea",self.outputpath)

        #press convert button
        proceed = self.driver.find_element(By.ID, "component-92")
        proceed.click()
        #wait until done converting
        wait = WebDriverWait(self.driver, timeout=90, poll_frequency=.2, ignored_exceptions=NoSuchElementException)
        wait.until(lambda d : self.driver.find_element(By.ID, "component-93").find_element(By.CLASS_NAME, "hide") or True)
        
        output = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.flac'):
                    output.append(os.path.join(root, file))
        return output

    def convert(self, path, model,truncate,feature):
        """Convert voice"""
        
        mode = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Model Inference')]")
        mode.click()
        
        #model
        self.WriteToField("component-6","input",f"{model}.pth")
        self.driver.find_element(By.ID, "component-6").find_element(By.CLASS_NAME, "svelte-qgtjkt").click()
        #Trancate
        self.WriteToField("component-15","input",truncate)
        #Audio path
        self.WriteToField("component-16","textarea",path)
        #index
        self.WriteToField("component-24","textarea",self.models[model]['index'])
        #feature
        self.WriteToField("component-26","input",feature)
        
        #press convert button
        proceed = self.driver.find_element(By.ID, "component-42")
        proceed.click()
        #wait until done converting
        wait = WebDriverWait(self.driver, timeout=90, poll_frequency=.2, ignored_exceptions=NoSuchElementException)
        wait.until(lambda d : self.driver.find_element(By.ID, "component-44").find_element(By.CLASS_NAME, "hide") or True)
        
        result = self.driver.find_element(By.CLASS_NAME, "svelte-eemfgq")
        return result.get_attribute('scr')
    
    def update_models(self):
        for root, dirs, files in os.walk("..\\server\\weights"):
            for file in files:
                if file.endswith('.pth'):
                    self.models[file[:file.rfind('.')]] = {'model':os.path.join(root, file), 'index':os.path.join(root, file[:file.rfind('.')] + '.index')}
    
    def cover(self, model,truncate,truncate_spread,feature=0.75,path=f"{os.getcwd()}\\audio"):
        truncate,truncate_spread,feature=int(truncate),int(truncate_spread),float(feature)
        output = self.separate(path)
        #for i in range(-truncate_spread,truncate_spread+1):
        result = self.convert(output, model, truncate, feature)
        print(result)
if __name__ == "__main__":
    inst = Cover()
    sleep(2)
    inst.cover('shaman',0,4)
    