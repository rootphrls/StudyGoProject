import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter.messagebox as tkmb
import time
import check_login as cl
import re

def simulate_login():
        progress['maximum'] = 100
        for i in range(101):
            time.sleep(0.02)  # Simulating some work being done
            progress['value'] = i
            progress.update()

def login():
    global username,password
    # new_window = ctk.CTkToplevel(root)
    # new_window.title("New Window")
    # new_window.geometry("1200x800")
    
    loading_label.pack()
    # simulate_login()
    simulate_login()
    loading_label.grid_forget()

    username = user_entry.get()
    password = user_pass.get()

    def validate_email(email):
        pattern = r'^[a-zA-Z0-9_.+-]+@gmail\.com$'
        return bool(re.match(pattern, email))
    
    def switch_to_new_page():
        #Destroy all the widgets from the previous page
        for widget in root.winfo_children():
            widget.destroy()
            root.after(10,root.destroy)
    
    if validate_email(username):
        if cl.check_info(username,password) == True:
            tkmb.showinfo(title="Login Succesful", message="You have logged in succesfully!")
            switch_to_new_page()
        else:
            tkmb.showerror(title="Login Failed", message="Invalid Username and password")
    else:
        tkmb.showerror(title="Wrong Format",message="Wrong Email Format Please Try Again")


    # if user_entry.get() == username and user_pass.get() == password:
    #     tkmb.showinfo(title="Login Succesful", message="You have logged in succesfully!")
    #     # ctk.CTkLabel(new_window,text="Geeks for Geeks is the best for learning anything").pack()
    # else:
    #     tkmb.showerror(title="Login Failed", message="Invalid username and password")



def show_entry():
    global loading_label,progress,small_image, small_image_label, user_entry, user_pass, button

    label.configure(font=("Tilt Neon",20),bg="#e9ecf2")
    label.place(relx=0.350,rely=0.1)

    resized_image = Image.open("studygo.png").resize((100,100))
    small_image = ImageTk.PhotoImage(resized_image)
    small_image_label = tk.Label(root, image=small_image)
    small_image_label.image = small_image
    small_image_label.place(relx=0.46,rely=0.2)

    user_entry = ctk.CTkEntry(master=frame, placeholder_text="Email")
    user_entry.configure(width = 200,height = 40)
    user_entry.place(relx=0.416,rely = 0.35)

    user_pass = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
    user_pass.configure(width = 200,height = 40)
    user_pass.place(relx=0.416,rely = 0.41)

    loading_label = ttk.Label(root, text="Gegevens Wordt Gecontroleerd",font=("Helvatica",12))
    progress = ttk.Progressbar(root,mode="determinate",length=200)
    progress.pack()

    button = ctk.CTkButton(master=frame, text="Login", command=login)
    button.place(relx=0.444,rely = 0.5)

    def test(event):
        login()

    root.bind("<Return>", test)





def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path:
        image = Image.open(file_path)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo

def start_animation():
    start_width = 10
    start_height = 10
    target_width = 600
    target_height = 400
    duration = 2000  # in milliseconds

    def animate():
        nonlocal start_width, start_height
        if start_width < target_width and start_height < target_height:
            start_width += 5
            start_height += 3
            resized_image = Image.open("studygo.png").resize((start_width, start_height), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized_image)
            label.config(image=photo)
            label.image = photo
            root.after(10, animate)
        else:
            # Start the shrink animation
            shrink_animation()

    animate()

def shrink_animation():
    target_width = 0
    target_height = 0
    duration = 2000  # in milliseconds

    def animate():
        nonlocal target_width, target_height
        if target_width > 0 or target_height > 0:
            target_width -= 5
            target_height -= 3
            resized_image = Image.open("studygo.png").resize((target_width, target_height), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized_image)
            label.config(image=photo)
            label.image = photo
            root.after(10, animate)
        else:
            # Remove the image
            label.config(image="")
            label.image = ""

    animate()

root = tk.Tk()
root.title("Login Page")
root.geometry("1200x800")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx = 40,fill = "both",expand= True)

label = tk.Label(master=frame,text="Sign into your StudyGo account")
label.pack()

start_animation()

root.after(3300,show_entry)


# # Create the button to upload image
# upload_button = tk.Button(root, text="Upload Image", command=upload_image)
# upload_button.pack()

root.mainloop()
