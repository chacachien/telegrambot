from os import read
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from datetime import datetime
import traceback
import sys


class Check_Web:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()
        self.url = 'https://datalace.org'
        self.username = 'demo1'
        self.password = 'Htech123@'
        self.ignore_exceptions = (
            NoSuchElementException, StaleElementReferenceException)

    def check_url(self):
        try:
            self.driver.get(self.url)
            print(f'The website {self.url} is up.')
            return True
        except Exception as e:
            print(f'Error connecting to {self.url}: {e}')
            return False

    def check_login(self):
        try:
            self.url += '/login'
            self.driver.get(self.url)
            time.sleep(5)
            input_user = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignore_exceptions).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[3]/form/div[1]/input')))
            # //*[@id="root"]/div/div/div[2]/form/div[1]/input
            input_user.send_keys(self.username)
            input_password = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignore_exceptions).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[3]/form/div[2]/input')))
            # //*[@id="root"]/div/div/div[3]/form/div[2]/input
            input_password.send_keys(self.password)
            WebDriverWait(self.driver, 10, ignored_exceptions=self.ignore_exceptions).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[3]/form/button'))).click()
            time.sleep(10)
            print(f'Login success.')
            return True
        except Exception as e:
            print(f'Error connecting to {self.url}: {e}')
            return False
    def visualize(self, user_inuts, path_file, root_path):
        file_name = os.path.basename(path_file)
        file_name = f"{file_name[:-4]}.txt"
        file_path = os.path.join(root_path, file_name)
        average_time_visual = 0
        hit_rate = 0 
        time_upload = 0
        try:
            time.sleep(5)
            input_btn = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignore_exceptions).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="exampleFormControlInput3"]')))

            input_btn.send_keys("")
            upload_btn=WebDriverWait(self.driver, 10, ignored_exceptions=self.ignore_exceptions).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="menu-button-:r4:"]')))
            time.sleep(5)
            actions = ActionChains(self.driver) 
            actions.move_to_element(upload_btn)
            time.sleep(1)
            upload_btn.click()
            time.sleep(3)

            start_time = time.time()
            input_file = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignore_exceptions).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="menu-list-:r4:-menuitem-:r5:"]/input')))
                
            # driver.execute_script("arguments[0].stype.display = 'block';", input_file)
            input_file.send_keys(path_file)

            time.sleep(3)

            # open_btn.click()
            j = 1
            for i in range(len(user_inuts)):
                print("user input at: ", user_inuts[i])
                with open(file_path, "a") as f:
                    f.write(f"| User input {i}: {user_inuts[i]}\n")
                time.sleep(20)
                # input_btn = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions).until(
                #     EC.element_to_be_clickable((By.XPATH, '//*[@id="chat4"]/div[3]/input')))
                start_time = time.time()
                upload_file_count = 0
                while True:
                    try:
                        input_btn = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignore_exceptions).until(
                            EC.element_to_be_clickable((By.XPATH, '//*[@id="exampleFormControlInput3"]')))
                        break
                    except:
                        print("wait for upload file ", upload_file_count)
                        if upload_file_count > 50:
                            print("Element does not exist or is not visible within the specified timeout.")
                            with open(file_path, "a") as f:
                                f.write(f"| => Error: Wait for upload file timeout!\n|\n")
                            break
                    upload_file_count +=1
                    time.sleep(1)
                if i == 0:
                    time_upload = time.time() - start_time
                    print("time upload: ", time_upload)
                input_btn.send_keys(user_inuts[i])
                WebDriverWait(self.driver, 10, ignored_exceptions=self.ignore_exceptions).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="chat4"]/div[3]/button[2]'))).click()
                c =1
                clicked = False
                while True:
                    try:
                        print("wait for load visulization")
                        load_icon_xpath = f'//*[@id="chat4"]/div[1]/div[1]/div[2]/div[{j}]/div[2]/div/div/p'
                        load_icon = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignore_exceptions).until(
                            EC.presence_of_element_located((By.XPATH, load_icon_xpath)))
                        #print("load_icon: ", load_icon)
                        time.sleep(3)
                        c+=1
                        if c > 50:
                            print("Element does not exist or is not visible within the specified timeout.")
                            with open(file_path, "a") as f:
                                f.write(f"| => Error: Wait for visualizing timeout!\n|\n")
                            break
                        print("load icon text1: ", load_icon.text)
                        if len(load_icon.text) > 0:
                            print("load icon text2: ", load_icon.text)
                            # if load_icon.text == "Sorry! I can't visualize it. Please try again!!!":
                            #     WebDriverWait(driver, 10, ignored_exceptions=ignored_exceptions).until(
                            #         EC.element_to_be_clickable((By.XPATH, '//*[@id="chat4"]/div[2]/button[3]'))).click()
                                
                            #     print("click regenerate")
                            # else:
                            time_vis = time.time() - start_time
                            average_time_visual += time_vis
                            hit_rate += 1
                            with open(file_path, "a") as f:
                                f.write(f"| + Time visualize: {time_vis}\n")
                                f.write(f"| => Result: Success!\n|\n")
                            break
                        print(c)
                    except Exception as e:
                        print(e)
                        c += 1
                        if c > 50:
                            print("Element does not exist or is not visible within the specified timeout.")
                            with open(file_path, "a") as f:
                                f.write(f"| => Error: Wait for visualizing timeout!\n|\n")
                            break
                        if not clicked:
                            sorry_text = WebDriverWait(self.driver, 10, ignored_exceptions=self.ignore_exceptions).until(
                                EC.presence_of_element_located((By.XPATH, f'//*[@id="chat4"]/div[1]/div[1]/div[2]/div[{j}]/div[2]/div/p')))
                                                                        # //*[@id="chat4"]/div[1]/div[1]/div[2]/div[1]/div[2]/div/p
                            if sorry_text.text == "Sorry! I can't visualize it. Please try again!!!":
                                WebDriverWait(self.driver, 10, ignored_exceptions=self.ignore_exceptions).until(
                                    EC.element_to_be_clickable((By.XPATH, '//*[@id="chat4"]/div[2]/button[3]'))).click()
                                time.sleep(3)
                                j = j +1
                                print("click regenerate")
                                clicked = True
                        else:
                            break        
                j = j +1
            log_entries = self.driver.get_log("browser")
            for entry in log_entries:
                with open(file_path, "a") as f:
                    f.write(f"| => Error from frontent (maybe not important): \n")
                    f.write(f"|\t \t + {str(entry)}\n")
            print("success: ", hit_rate)
            print("total visual: ", j)

            return time_upload, average_time_visual/len(user_inuts), hit_rate/(j-1)

        except Exception as e:
            traceback.print_exc()
            exc_type, _, _ = sys.exc_info()
            exception_name = exc_type.__name__

            print(f"The exception name is: {exception_name}")
            with open(file_path, "a") as f:
                f.write(f"| => Error from selenium: {str(exception_name)}\n|\n")
            return None, None, None

    def check_visualize(self):
        root = os.path.dirname(os.path.abspath(__file__))
        print(root)
        folder = f"{root}/data"
        files = [os.path.join(folder, file) for file in os.listdir(folder)]
        root_path = f"{root}/log"
        test_time = datetime.now().strftime('%H:%M:%S')
        test_date = datetime.now().strftime('%d-%m-%Y')
        date_folder = os.path.join(root_path, test_date)
        if not os.path.exists(date_folder):
            os.mkdir(date_folder)

        file_path = os.path.join(date_folder, test_time)
        os.mkdir(file_path)
        root_path = os.path.join(root_path, file_path)
        all_time_uploads = []
        all_average_time_visuals = []
        all_hit_rates = []

        for file in files:
            file_name_log = os.path.basename(file)
            user_inputs = []
            with open(f"{root}/question/{file_name_log[:-4]}.txt", "r") as f:
                lines = f.readlines()
                user_inputs += [line.strip() for line in lines if line.strip()]
            print(user_inputs)
            file_name_log, file_name_web = f"{file_name_log[:-4]}.txt" , f"{file_name_log[:-4]}.html"
            file_path_log = os.path.join(root_path, file_name_log)
            file_path_web = os.path.join(root_path, file_name_web)
            
            time_upload, average_time_visual, hit_rate = self.visualize(user_inputs, file, root_path)


            if time_upload == None:
                with open(file_path_log, "a") as f:
                    f.write(f"|\t Result of this testcase: Fail! \n")
                return None, None, None
            else:
                with open(file_path_log, "a") as f:
                    f.write(f"|\t Time upload file: {time_upload}\n")
                    f.write(f"|\t Average time visual: {average_time_visual}\n")
                    f.write(f"|\t Hit rate: {hit_rate}\n")
                    f.write(f"|\t Result of this testcase: Suceess! \n")
            with open(file_path_log, "a") as f:
                f.write(f"|\t Test at: {datetime.now()}\n")
                f.write(f"---------------------------------------------\n")
            page = self.driver.page_source.encode('utf-8') 
            file_ = open(file_path_web, 'wb') 
            file_.write(page) 
                # Append metrics to lists
            all_time_uploads.append(time_upload)
            all_average_time_visuals.append(average_time_visual)
            all_hit_rates.append(hit_rate)
        # Calculate averages
        avg_time_upload = sum(filter(None, all_time_uploads)) / len(all_time_uploads) if all_time_uploads else None
        avg_average_time_visual = sum(filter(None, all_average_time_visuals)) / len(all_average_time_visuals) if all_average_time_visuals else None
        avg_hit_rate = sum(filter(None, all_hit_rates)) / len(all_hit_rates) if all_hit_rates else None

        # Write averages to the final log file
        final_log_path = os.path.join(root_path, "final_log.txt")
        with open(final_log_path, "a") as f:
            f.write(f"|\t Average Time upload file: {avg_time_upload}\n")
            f.write(f"|\t Average Average time visual: {avg_average_time_visual}\n")
            f.write(f"|\t Average Hit rate: {avg_hit_rate}\n")
            f.write(f"|\t Test at: {datetime.now()}\n")
            f.write(f"---------------------------------------------\n")
        return avg_time_upload, avg_average_time_visual, avg_hit_rate
            
    def close(self):
        self.driver.quit()
        print("Close browser")