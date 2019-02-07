from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import mysql.connector
from selenium.webdriver.firefox.options import Options


def run_scraping(url, os_name):
    success = True
    try:
        # Start Browser
        browser = webdriver.Firefox()
        browser.get(url)

        # Connect to database
        mydb2 = mysql.connector.connect(
            host="qpairboto.cnryqwkkelel.us-east-1.rds.amazonaws.com",
            user="rivetcopt",
            passwd="rivetcopt",
            database="copt"
        )
        cur2 = mydb2.cursor()

        # Find list of regions
        region_list_elem = browser.find_element_by_xpath("//*[@id='region-selector']")

        # Wait for element clickable
        WebDriverWait(browser, 30).until(EC.element_to_be_clickable, (By.XPATH, "//*[@id='region-selector']"))

        # Click on the regions List
        region_list_elem.click()

        # Iterate over the region optgroup list
        for k, region_opt_group in enumerate(
                BeautifulSoup(region_list_elem.get_attribute('innerHTML'), "html5lib").findAll('optgroup')):

            # Wait for optgroup element presence
            WebDriverWait(browser, 30).until(EC.presence_of_element_located, (By.XPATH,
                                                                              f"//*[@id='region-selector']/optgroup[1]"))

            # Find the optgroup element
            region_opt_group_elem = browser.find_element_by_xpath(f"//*[@id='region-selector']/optgroup[1]")

            # Iterate over the Region option list
            for l, region_option in enumerate(
                    BeautifulSoup(region_opt_group_elem.get_attribute('innerHTML'), "html5lib").findAll('option')):

                # Wait for optgroup element presence
                WebDriverWait(browser, 30).until(EC.element_to_be_clickable, (By.XPATH,
                                                                              f"//*[@id='region-selector']/optgroup[1]/option[{l + 1!r}]"))

                # Find the Region Option element
                region_option_elem = browser.find_element_by_xpath(
                    f"//*[@id='region-selector']/optgroup[1]/option[{l + 1!r}]")

                # Click on the Region option element
                region_option_elem.click()

                # Find list of Display Pricing
                display_list_elem = browser.find_element_by_xpath("//*[@id='pricing-display-by-dropdown']")

                # Wait for element clickable
                WebDriverWait(browser, 30).until(EC.element_to_be_clickable,
                                                 (By.XPATH, "//*[@id='pricing-display-by-dropdown']"))

                # Click on the display pricing List
                display_list_elem.click()

                # Iterate over the display pricing options
                for m, display_option in enumerate(
                        BeautifulSoup(display_list_elem.get_attribute('innerHTML'), "html5lib").findAll('option')):

                    # Find the option element
                    display_option_elem = browser.find_element_by_xpath(
                        f"//*[@id='pricing-display-by-dropdown']/option[{m + 1!r}]")

                    # Wait for option element presence
                    WebDriverWait(browser, 30).until(EC.element_to_be_clickable, (By.XPATH,
                                                                                  f"//*[@id='pricing-display-by-dropdown']/option[{m + 1!r}]"))

                    # Click on the display option element
                    display_option_elem.click()

                    # Find the category_list_elem
                    category_list_elem = browser.find_element_by_xpath("//*[@id='vm-categories']/div[1]/div[2]/ul")

                    # Iterate over the category options
                    for n, category_option in enumerate(
                            BeautifulSoup(category_list_elem.get_attribute('innerHTML'), "html5lib").findAll('button')):

                        # Ignore first one as it is all
                        if n != 0:
                            # Find Category Option element
                            category_option_elem = browser.find_element_by_xpath(
                                f"//*[@id='vm-categories']/div[1]/div[2]/ul/li[{n + 1!r}]/button")

                            # Click on the category option element
                            browser.execute_script("return arguments[0].click()", category_option_elem)

                            # Find Id of category div which has the content
                            cat_option_div_id = str(category_option_elem.text).lower().replace(' ', '-')

                            # Wait for option element presence
                            WebDriverWait(browser, 30).until(EC.presence_of_element_located, (By.XPATH,
                                                                                              f"//*[@id={cat_option_div_id!r}][2]"))

                            # Find the cat_sub_types wrapper
                            cat_sub_types_wrapper = browser.find_element_by_xpath(f"//*[@id={cat_option_div_id!r}][2]")

                            # Iterate over the category subtype options
                            for o, cat_sub_type in enumerate(
                                    BeautifulSoup(cat_sub_types_wrapper.get_attribute('innerHTML'), "html5lib").findAll(
                                            'h3')):

                                # Find the table
                                cat_sub_type_table = BeautifulSoup(cat_sub_types_wrapper.get_attribute('innerHTML'),
                                                                   "html5lib").findAll('table')

                                # If pricing is unavailable skip
                                if "pricing-unavailable" not in cat_sub_type_table[o].attrs['class']:

                                    # find the body of table
                                    cat_sub_type_tbody = cat_sub_type_table[o].find('tbody')

                                    # Find all the headings
                                    heading_list = [heading.text.strip() for heading in
                                                    cat_sub_type_table[o].findAll('th')]

                                    # Set all the index to zero
                                    instance_column_number = 0
                                    activeCPU_column_number = 0
                                    cpu_column_number = 0
                                    core_column_number = 0
                                    gpu_column_number = 0
                                    nvm_column_number = 0
                                    ram_column_number = 0
                                    temp_column_number = 0
                                    pay_column_number = 0
                                    one_year_column_number = 0
                                    three_year_column_number = 0
                                    azure_year_column_number = 0

                                    # Set the index according to the columns
                                    for column_index, heading in enumerate(heading_list):
                                        if heading == "Instance":
                                            instance_column_number = column_index + 1
                                        elif heading == "Active vCPU /  Underlying vCPU":
                                            activeCPU_column_number = column_index + 1
                                        elif heading == "vCPU":
                                            cpu_column_number = column_index + 1
                                        elif heading == "Core":
                                            core_column_number = column_index + 1
                                        elif heading == "GPU":
                                            gpu_column_number = column_index + 1
                                        elif heading == "NVMe Disk":
                                            nvm_column_number = column_index + 1
                                        elif heading == "RAM":
                                            ram_column_number = column_index + 1
                                        elif heading == "Temporary storage":
                                            temp_column_number = column_index + 1
                                        elif heading == "Pay as you go":
                                            pay_column_number = column_index + 1
                                        elif heading == "One year reserved(% Savings)":
                                            one_year_column_number = column_index + 1
                                        elif heading == "Three year reserved(% Savings)":
                                            three_year_column_number = column_index + 1
                                        elif heading == "3 year reserved with Azure Hybrid Benefit for SQL Server and Windows Server(% Savings)":
                                            azure_year_column_number = column_index + 1

                                    # find all the rows
                                    for cat_sub_type_row in cat_sub_type_tbody.findAll('tr'):

                                        # Set all the variables as empty
                                        instance_type = ""
                                        active = ""
                                        underlying = ""
                                        cpu = ""
                                        core = ""
                                        ram = ""
                                        temp_storage = ""
                                        pay = ""
                                        gpu = ""
                                        nvm = ""
                                        one_year = ""
                                        one_year_savings = ""
                                        three_year = ""
                                        three_year_savings = ""
                                        azure_hybrid = ""
                                        azure_hybrid_savings = ""

                                        # Find all the values
                                        instance_type = cat_sub_type_row.find(
                                            'td', attrs={'class': f"column-{instance_column_number!r}"}).contents[
                                            0].strip()

                                        # Check if cpu column is present
                                        if cpu_column_number != 0:
                                            cpu = cat_sub_type_row.find(
                                                'td', attrs={'class': f"column-{cpu_column_number!r}"}).contents[
                                                0].strip()

                                        # Check if cpu column is present
                                        if activeCPU_column_number != 0:
                                            active_contents = cat_sub_type_row.find(
                                                'td', attrs={'class': f"column-{activeCPU_column_number!r}"}).contents[
                                                0].split('/')
                                            active = active_contents[0].strip()
                                            underlying = active_contents[1].strip()

                                        # Check if core column is present
                                        if core_column_number != 0:
                                            core = cat_sub_type_row.find(
                                                'td', attrs={'class': f"column-{core_column_number!r}"}).contents[
                                                0].strip()

                                        # Check if gpu column is present
                                        if gpu_column_number != 0:
                                            gpu = cat_sub_type_row.find(
                                                'td', attrs={'class': f"column-{gpu_column_number!r}"}).contents[
                                                0].strip()

                                        # Check if nvm column is present
                                        if nvm_column_number != 0:
                                            nvm = cat_sub_type_row.find(
                                                'td', attrs={'class': f"column-{nvm_column_number!r}"}).contents[
                                                0].strip()

                                        ram = cat_sub_type_row.find(
                                            'td', attrs={'class': f"column-{ram_column_number!r}"}).contents[0].strip()
                                        temp_storage = cat_sub_type_row.find(
                                            'td', attrs={'class': f"column-{temp_column_number!r}"}).contents[0].strip()

                                        pay_td_elem = cat_sub_type_row.find(
                                            'td', attrs={'class': f"column-{pay_column_number!r}"})

                                        pay_td_elem_span = pay_td_elem.find('span')

                                        if pay_td_elem_span != None:
                                            if 'data-has-valid-price' in pay_td_elem_span.attrs and pay_td_elem_span[
                                                'data-has-valid-price'] == "true":
                                                pay = pay_td_elem_span.text.strip()
                                            else:
                                                pay = pay_td_elem_span.text.strip()
                                        else:
                                            pay = pay_td_elem.text.strip()

                                        one_year_td_elem = cat_sub_type_row.find(
                                            'td', attrs={'class': f"column-{one_year_column_number!r}"})
                                        one_year_td_elem_span_list = one_year_td_elem.findAll('span')
                                        if len(one_year_td_elem_span_list) != 0:
                                            if 'data-has-valid-price' in one_year_td_elem_span_list[0].attrs and \
                                                    one_year_td_elem_span_list[0]['data-has-valid-price'] == "true":
                                                one_year = one_year_td_elem_span_list[0].text.strip()
                                                one_year_savings = one_year_td_elem_span_list[1].text.strip()
                                            else:
                                                one_year = one_year_td_elem_span_list[0].text.strip()
                                        else:
                                            one_year = one_year_td_elem.text.strip()
                                            one_year_savings = ""

                                        three_year_td_elem = cat_sub_type_row.find(
                                            'td', attrs={'class': f"column-{three_year_column_number!r}"})

                                        three_year_td_elem_span_list = three_year_td_elem.findAll('span')

                                        if len(three_year_td_elem_span_list) != 0:
                                            if 'data-has-valid-price' in three_year_td_elem_span_list[0].attrs and \
                                                    three_year_td_elem_span_list[0]['data-has-valid-price'] == "true":
                                                three_year = three_year_td_elem_span_list[0].text.strip()
                                                three_year_savings = three_year_td_elem_span_list[1].text.strip()
                                            else:
                                                three_year = three_year_td_elem_span_list[0].text.strip()
                                        else:
                                            three_year = three_year_td_elem.text.strip()
                                            three_year_savings = ""

                                        # Check if there is azure hybrid column and set the value
                                        if (azure_year_column_number != 0):
                                            azure_hybrid_td_elem = cat_sub_type_row.find(
                                                'td', attrs={'class': f"column-{azure_year_column_number!r}"})

                                            azure_hybrid_td_elem_span_list = azure_hybrid_td_elem.findAll('span')

                                            if len(azure_hybrid_td_elem_span_list) != 0:
                                                if 'data-has-valid-price' in azure_hybrid_td_elem_span_list[0].attrs and \
                                                        azure_hybrid_td_elem_span_list[0][
                                                            'data-has-valid-price'] == "true":
                                                    azure_hybrid = azure_hybrid_td_elem_span_list[0].text.strip()
                                                    azure_hybrid_savings = azure_hybrid_td_elem_span_list[
                                                        1].text.strip()
                                                else:
                                                    azure_hybrid = azure_hybrid_td_elem_span_list[0].text.strip()
                                            else:
                                                azure_hybrid = azure_hybrid_td_elem.text.strip()
                                                azure_hybrid_savings = ""

                                        # print(os_name,region_option.text.strip(),display_option.text.strip(),category_option.text.strip(), cat_sub_type.text.strip(), instance_type, cpu, ram, temp_storage, pay, one_year, one_year_savings, three_year, three_year_savings, azure_hybrid, azure_hybrid_savings)

                                        # Insert Data
                                        sql = """
                                        INSERT INTO Test
                                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                                        """
                                        cur2.execute(sql,
                                                     [os_name, region_option.text.strip(), display_option.text.strip(),
                                                      category_option.text.strip(), cat_sub_type.text.strip(),
                                                      instance_type, active, underlying, cpu, core, ram, gpu, nvm,
                                                      temp_storage, pay, one_year, one_year_savings, three_year,
                                                      three_year_savings, azure_hybrid, azure_hybrid_savings])
                                        # Save data to database
                                        mydb2.commit()

    except Exception as err:
        print("Exception at")
        print(err)
        success = False
        # To Inform where it failed
        print(os_name, region_option.text.strip(), display_option.text.strip(), category_option.text.strip(),
              ' '.join(cat_sub_type.text.strip().split()), instance_type, active, underlying, cpu, core, ram, gpu, nvm,
              temp_storage, pay, one_year, one_year_savings, three_year, three_year_savings, azure_hybrid,
              azure_hybrid_savings)

    finally:
        browser.close()
        mydb2.close()
        return success