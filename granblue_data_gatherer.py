from logger import get_logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException
import time
import csv

class GranblueDataGatherer():
    def __init__(self, character) -> None:
        # get the logger
        self.logger = get_logger()

        # setup the webdriver
        try:
            # specify chromedriver path (will also need to alter the relevant test if changed)
            self.chrome_driver_path = 'C:/Development/chromedriver.exe'
            self.s = Service(self.chrome_driver_path)
            self.driver = webdriver.Chrome(service=self.s)
            self.moveList = []
            self.character = character
        
        except (WebDriverException, SessionNotCreatedException, PermissionError) as e:
            self.logger.error(f"An error occurred during the setup of the webdriver: {e}")
                    
    def go_to_character_page(self):
        # url has title case for character names
        self.driver.get(f'https://www.dustloop.com/w/GBVSR/{self.character.title()}')
        self.driver.maximize_window()
        time.sleep(3)
        
    def process_version(self, table):
        # the final data list
        rows_processed = []
        
        # get all the rows in the table
        rows = table.find_elements(By.TAG_NAME, "tr")
        # for each row in the table:
        for row in rows:
            row_data=[]
            # get all children and add their text to row_data
            children = row.find_elements(By.XPATH, "*")
            for child in children:
                row_data.append(child.text)
            # if the data is unique (not a header again) add it to the final list  
            if row_data not in rows_processed:
                rows_processed.append(row_data)              
            
        # change fieldname from "Version" to "Name"
        rows_processed[0][0] = "Name"
        
        # add the key:value pairs to the dict since everything matches up now
        for attack in rows_processed[1:]:
            new_move = dict(zip(rows_processed[0], attack))
            self.moveList.append(new_move)  
            self.logger.info(f"Processed - {new_move['Name']}")    
    
    def finish_process(self, name_of_move, rows):
        # finished row data
        row_processed = []
        
        # for each row in the table:
        for row in rows:
            row_data=[]
            # get all children and add their text to row_data
            children = row.find_elements(By.XPATH, "*")
            for child in children:
                row_data.append(child.text)
            row_processed.append(row_data)
        
        # the headers are the first list, and the data is the second         
        new_move = {"Name": name_of_move.text, **dict(zip(row_processed[0], row_processed[1]))}
        return new_move
    
    # targets the appropriate name elements for normals
    def process_normal(self, table):
        # for every table, go to the ancestor that is on the same level as the preceding
        name_of_move = table.find_element(By.XPATH, "ancestor::div[contains(@class, 'attack-container')]/preceding-sibling::h4[1]/span[@class='mw-headline']")
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        new_move = self.finish_process(name_of_move, rows)

        # add the move to the list
        self.moveList.append(new_move)       
        self.logger.info(f"Processed - {new_move['Name']}") 
           
    # targets the appropriate elements for names in an 'input-badge'
    def process_badge_normal(self, table):
        # for every table, go to the ancestor that is on the same level as the preceding 
        name_of_move = table.find_element(By.XPATH, "ancestor::div[contains(@class, 'attack-container')]/preceding-sibling::p[1]/span[@class='input-badge']")
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        new_move = self.finish_process(name_of_move, rows)
        
        # add the move to the list
        self.moveList.append(new_move)
        self.logger.info(f"Processed - {new_move['Name']}")                
    
    # targets the appropriate elements for universal move names
    def process_universal_normal(self, table):
        # for every table, go to the ancestor that is on the same level as the preceding 
        name_of_move = table.find_element(By.XPATH, "ancestor::div[contains(@class, 'attack-container')]/preceding-sibling::h3[1]/span/big")
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        new_move = self.finish_process(name_of_move, rows)
        
        # add the move to the list
        self.moveList.append(new_move)   
        self.logger.info(f"Processed - {new_move['Name']}")
        
    def handle_section(self, section_id: str):
        try:
            moves_data = self.driver.find_elements(By.CSS_SELECTOR, f"#section-collapsible-{section_id} div.attack-container .moveTable")
            moves_data = [data for data in moves_data if data.is_displayed()]
            if len(moves_data) == 0:
                raise ValueError
        except ValueError:
            self.logger.error(f"No move tables found in {section_id}")
        
        self.logger.info(f"Processing section {section_id}")   
        
        for table in moves_data:
            if len(table.find_elements(By.TAG_NAME, "tr")) > 2:
                self.process_version(table)  
            else:
                if section_id == 2:
                    self.process_normal(table)
                elif section_id == 3:
                    self.process_badge_normal(table)
                elif section_id == 4:
                    self.process_universal_normal(table)
                else:
                    self.process_badge_normal(table)    
                                     
        self.logger.info(f"Finished processing section {section_id}")     
                      
    def create_csv(self):
        # opens an existing file and overwrites it, or creates a new one(useful since game patches will change frame data)
        with open(f"character_frame_data/{self.character}.csv", "a") as file:
            file.truncate(0)
            header = ["Name", "Damage", "Guard", "Startup", "Active", "Recovery", "On Block", "On Hit", "Invuln"]
            csv_writer = csv.DictWriter(file, fieldnames=header)
            csv_writer.writeheader()
            for move in self.moveList:
                csv_writer.writerow(move)
        self.logger.info(f"csv file for {self.character} has been created!")