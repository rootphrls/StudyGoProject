from login_page import *
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter.messagebox as tkmb
import time
import check_login as cl
import re
from subjects import *
import pytesseract
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

def get_entrys():

    description_label = tk.Label(frame, text=usage_description,font=("Helvatica",12),height=25,width=40)
    description_label.place(relx=0.65,rely=0.01)
    note_label = tk.Label(frame, text=note_description,font=("Helvatica",12),height=14,width=40,fg="red")
    note_label.place(relx=0.65,rely=0.4)

    placeholder_subject = tk.StringVar(frame)
    placeholder_subject.set("Kies een vak")

    sub_select = tk.OptionMenu(frame,placeholder_subject,*subjects_list)
    sub_select.config(width=30,height=2,font=("Tilt Neon",10))
    sub_select.place(relx=0.02,rely=0.2)

    title_entry = ctk.CTkEntry(master=frame, placeholder_text="Geef je lijst een titel",font=("Poppins",20),width=250,height=35)
    title_entry.place(relx = 0.02, rely = 0.3)

    def upload_image():
        global file_path
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            success_label = tk.Label(frame, text="Upload succesful!",font=("Helvatica",12),fg="green")
            success_label.place(relx=0.25,rely=0.4)

    upload_button = tk.Button(root, text="Upload Image",command=upload_image,width=30,height=2)
    upload_button.place(relx=0.06,rely=0.4)

    def start():
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        words = text.split()
        title = title_entry.get()
        driver = webdriver.Firefox()
        wait = WebDriverWait(driver,3)
        subject = placeholder_subject.get()

        driver.get("https://studygo.com/nl/learn/sign-in")

        username_input = wait.until(EC.element_to_be_clickable((By.NAME,"email")))
        username_input = driver.find_element(By.NAME,"email")
        username_input.send_keys(username)

        password_input = wait.until(EC.element_to_be_clickable((By.NAME,"password")))
        password_input = driver.find_element(By.NAME,"password")
        password_input.send_keys(password)

        login_button = driver.find_element(By.XPATH, '/html/body/div[1]/main/div[2]/div/div/div/div[1]/form/div[3]/button')
        login_button.click()

        nieuw = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/div/div[1]/div/div[1]/button')))
        nieuw.click()

        lijst = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/div[1]/div/div[1]/div/div[2]/div/div[2]/div[1]/div/div/div[1]/button')))
        lijst.click()

        expand = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="root"]/main/div/div[1]/form/div[1]/div[1]/span[3]')))
        expand.click()

        #Find all elements under the parent div
        alle_vakken = driver.find_elements(By.XPATH, "//div[@class='section-item']/*")

        #Iterate through the elements and check their text
        for element in alle_vakken:
            driver.execute_script("arguments[0].scrollIntoView();",element)
            if element.text == subject:
                element.click()
                break

        set_title = driver.find_element(By.NAME, "list-title")
        set_title.send_keys(title)

        time.sleep(0.5)



        how_many_times = len(words) // 2 - 10
        for i in range(how_many_times):
            add_space = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[1]/form/section/button')
            add_space.click()
            # driver.execute_script("arguments[0].scrollIntoView();", element)

        child_elements = driver.find_elements(By.XPATH, "//div[@class='input-wrap first-input']/*")

        #Iterate through the child elements
        i = 0
        for element in child_elements:
            data_name = element.get_attribute("data-name")
            if data_name:
                element.send_keys(words[i])
                i += 2

        child_elements = driver.find_elements(By.XPATH, "//div[@class='input-wrap']/*")

        i = 1
        for element in child_elements:
            data_name = element.get_attribute("data-name")
            if data_name:
                element.send_keys(words[i])
                i += 2
        time.sleep(0.3)

        aanmaken = driver.find_element(By.XPATH, '//*[@id="root"]/main/div/div[2]/div/div/div[2]/button[2]')
        aanmaken.click()
        time.sleep(5)

        driver.close()
        driver.quit()
        

    processxstart= tk.Button(frame, text="START THE PROCESS",command=start,font=("Pacifico",14))
    processxstart.place(relx=0.4, rely=0.7)


root = tk.Tk()
root.title("StudyGo Project")
root.geometry("1200x800")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20,padx=40,fill ="both",expand = True)

label = tk.Label(root, text="Create A New Study Set", font=("Tilt Neon", 20))
label.place(relx=0.39, rely=0.1)

root.after(1,get_entrys)

root.mainloop()

