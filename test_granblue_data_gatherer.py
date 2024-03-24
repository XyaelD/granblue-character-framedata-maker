import pytest

from unittest.mock import Mock, patch, MagicMock
from granblue_data_gatherer import GranblueDataGatherer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# patch creates MagicMock objects for the Service and webdriver, and  have to be given parameter names even if unused
@pytest.fixture
@patch('granblue_data_gatherer.Service')
@patch('granblue_data_gatherer.webdriver.Chrome')
def gbg(mock_service, mock_driver):
        character = "Gran"
        return GranblueDataGatherer(character)

# checks that the GranblueDataGatherer Class is initialized correctly for testing
def test_init(gbg):
    assert gbg.chrome_driver_path == 'C:/Development/chromedriver.exe'
    assert isinstance(gbg.s, MagicMock)
    assert isinstance(gbg.driver, MagicMock)
    assert gbg.moveList == []
    assert gbg.character == "Gran"

# checks that the webdriver goes to the correct page with the correct variable a single time                   
def test_go_to_character_page(gbg):
    target_url = f'https://www.dustloop.com/w/GBVSR/{gbg.character.title()}'

    gbg.go_to_character_page()

    gbg.driver.get.assert_called_once_with(target_url)
    gbg.driver.maximize_window.assert_called_once()

# checks that found tables of given lengths are handled correctly
def test_handle_section(gbg):
    
    mock_find_elements = gbg.driver.find_elements
    
    # create two tables for testing of length 5 and 2 for number of rows returned
    mock_table_greater = MagicMock()
    mock_table_equal = MagicMock()
    mock_table_greater.is_displayed.return_value = True
    mock_table_equal.is_displayed.return_value = True
    mock_table_greater.find_elements.return_value = [MagicMock() for _ in range(5)]
    mock_table_equal.find_elements.return_value = [MagicMock() for _ in range(2)]
    
    # mock that the tables are found
    mock_find_elements.return_value = [mock_table_greater, mock_table_equal]
    
    # mock the methods inner methods for each table
    with patch.object(gbg, 'process_version') as mock_pv, patch.object(gbg, 'process_universal_normal') as mock_pun:
        gbg.handle_section(4)
        
        mock_find_elements.assert_called_once_with(By.CSS_SELECTOR, f"#section-collapsible-4 div.attack-container .moveTable")
        assert len(mock_table_greater.find_elements.return_value) == 5
        assert len(mock_table_equal.find_elements.return_value) == 2
        mock_pv.assert_called_once_with(mock_table_greater)
        mock_pun.assert_called_once_with(mock_table_equal)

def test_finish_process(gbg):

    mock_rows = MagicMock()
    mock_row1 = MagicMock()
    mock_row1.find_elements.return_value = [MagicMock(text="Damage"), MagicMock(text="Guard")]
    mock_row2 = MagicMock()
    mock_row2.find_elements.return_value = [MagicMock(text="600"), MagicMock(text="Mid")]
    mock_rows = [mock_row1, mock_row2]
    
    new_move_name = MagicMock(text="66L")
    
    result = gbg.finish_process(new_move_name, mock_rows)
    
    assert result == {"Name": "66L", "Damage": "600", "Guard": "Mid"}
    mock_row1.find_elements.assert_called_once()
    mock_row2.find_elements.assert_called_once()



    
     
     