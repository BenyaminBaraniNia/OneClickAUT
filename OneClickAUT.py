import customtkinter as ctk
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from cryptography.fernet import Fernet
import time
import json
import os
import sys


PROFILE_FILE = "profiles.json"
KEY_FILE = "key.key"

# Generate or load encryption key
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    else:
        with open(KEY_FILE, "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

encryptor = load_key()



class StudentPortalApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OneClickAUT (v1.0.0)")
        self.geometry("300x580")
        #self.iconbitmap("AUT.ico")



        # Get the base path for the executable or script
        if getattr(sys, 'frozen', False):
            # Running as a packaged executable
            base_path = sys._MEIPASS
        else:
            # Running as a script
            base_path = os.path.dirname(os.path.abspath(__file__))

        # Construct the full path to the icon file
        icon_path = os.path.join(base_path, "AUT.ico")

        # Set the application icon
        self.iconbitmap(icon_path)




        # Prevent the window from being resized
        self.resizable(False, False)  # Disable resizing in both width and height
        
        # Set dark theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Informational Text at the Top
        self.label_info_top = ctk.CTkLabel(self, text="Welcome to the OneClickAUT", font=("Arial", 14, "bold"))
        self.label_info_top.pack(pady=(20, 5))  # Add space at the top

        self.label_info_instructions = ctk.CTkLabel(self, text="Please enter your credentials below:", font=("Arial", 12))
        self.label_info_instructions.pack(pady=6)  # Add space below the instructions

        # Username Entry with Placeholder
        self.entry_username = ctk.CTkEntry(self, placeholder_text="Username")
        self.entry_username.pack(pady=10)
        self.entry_username.bind("<FocusIn>", lambda event: self.clear_placeholder(event, self.entry_username, "Username"))
        self.entry_username.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.entry_username, "Username"))

        # Password Entry with Placeholder
        self.entry_password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=10)
        self.entry_password.bind("<FocusIn>", lambda event: self.clear_placeholder(event, self.entry_password, "Password"))
        self.entry_password.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.entry_password, "Password"))

        # Student Number Entry with Placeholder
        self.entry_student_number = ctk.CTkEntry(self, placeholder_text="Student Number")
        self.entry_student_number.pack(pady=10)
        self.entry_student_number.bind("<FocusIn>", lambda event: self.clear_placeholder(event, self.entry_student_number, "Student Number"))
        self.entry_student_number.bind("<FocusOut>", lambda event: self.add_placeholder(event, self.entry_student_number, "Student Number"))

        # Remember Me
        self.remember_var = tk.BooleanVar()
        self.remember_check = ctk.CTkCheckBox(self, text="Remember Me", variable=self.remember_var)
        self.remember_check.pack(pady=15)

        # Degree Selection
        self.degree_var = tk.StringVar(value="M.Sc")
        self.label_degree = ctk.CTkLabel(self, text="Select Portal:")
        self.label_degree.pack()
        

        # Customized Radio Buttons
        self.radio_bsc = ctk.CTkRadioButton(
            self, 
            text="B.Sc", 
            variable=self.degree_var, 
            value="B.Sc", 
            command=self.load_profile,
            width=5,  # Smaller width
            height=5,  # Smaller height
            fg_color="#1f6aa5",  # Blue color when selected
            border_color="#ffffff",  # Blue ring color
            border_width_unchecked=7,  # Thickness of the ring when unchecked
            border_width_checked=7  # Thickness of the ring when checked
        )
        self.radio_bsc.pack(pady=6)


        self.radio_msc = ctk.CTkRadioButton(
            self, 
            text="M.Sc", 
            variable=self.degree_var, 
            value="M.Sc", 
            command=self.load_profile,
            width=5,  # Smaller width
            height=5,  # Smaller height
            fg_color="#1f6aa5",  # Blue color when selected
            border_color="#ffffff",  # Blue ring color
            border_width_unchecked=7,  # Thickness of the ring when unchecked
            border_width_checked=7  # Thickness of the ring when checked
        )
        self.radio_msc.pack(pady=6)


        self.radio_phd = ctk.CTkRadioButton(
            self, 
            text="Ph.D", 
            variable=self.degree_var, 
            value="Ph.D", 
            command=self.load_profile,
            width=5,  # Smaller width
            height=5,  # Smaller height
            fg_color="#1f6aa5",  # Blue color when selected
            border_color="#ffffff",  # Blue ring color
            border_width_unchecked=7,  # Thickness of the ring when unchecked
            border_width_checked=7  # Thickness of the ring when checked
        )
        self.radio_phd.pack(pady=10)


        # Load saved profile if exists
        self.load_profile()

        # Start Button
        self.start_button = ctk.CTkButton(self, text="Log in", command=self.start_script)
        self.start_button.pack(pady=20)


        # Developer Info (moved to bottom)
        self.label_info = ctk.CTkLabel(self, text="Developed by: Benyamin Barani Nia", font=("Arial", 12))
        self.label_info.pack(pady=5)

        # Combined Website and Github Links
        self.links_frame = ctk.CTkFrame(self)
        self.links_frame.pack(pady=2)

        # Website Link
        self.label_website = ctk.CTkLabel(
            self.links_frame, 
            text="Website", 
            cursor="hand2", 
            font=("Arial", 12),
            text_color="#1f6aa5"  # Blue color for the link
        )
        self.label_website.pack(side="left", padx=(0, 5))  # Add padding between links
        self.label_website.bind("<Button-1>", lambda event: self.open_website())

        # Separator
        self.label_separator = ctk.CTkLabel(self.links_frame, text="|", font=("Arial", 12))
        self.label_separator.pack(side="left", padx=(0, 5))  # Add padding between links

        # Github Link
        self.label_github = ctk.CTkLabel(
            self.links_frame, 
            text="Github", 
            cursor="hand2", 
            font=("Arial", 12),
            text_color="#1f6aa5"  # Blue color for the link
        )
        self.label_github.pack(side="left")
        self.label_github.bind("<Button-1>", lambda event: self.open_github())


    def clear_placeholder(self, event, entry_widget, placeholder):
        """Clear the placeholder text when the entry widget is focused."""
        if entry_widget.get() == placeholder:
            entry_widget.delete(0, tk.END)
            if entry_widget == self.entry_password:  # Show asterisks for password field
                entry_widget.configure(show="*")

    def add_placeholder(self, event, entry_widget, placeholder):
        """Add placeholder text back if the entry widget is empty."""
        if entry_widget.get() == "":
            entry_widget.insert(0, placeholder)
            if entry_widget == self.entry_password:  # Hide asterisks for placeholder
                entry_widget.configure(show="")        

    def open_website(self):
        """Open the Website link."""
        os.system("start https://www.BenWrites.ir/")

    def open_github(self):
        """Open the Github link."""
        os.system("start https://github.com/BenyaminBaraniNia")


    def encrypt_password(self, password):
        return encryptor.encrypt(password.encode()).decode()

    def decrypt_password(self, encrypted_password):
        return encryptor.decrypt(encrypted_password.encode()).decode()

    def save_profile(self, username, password, student_number, degree):
        if os.path.exists(PROFILE_FILE):
            with open(PROFILE_FILE, "r") as file:
                data = json.load(file)
        else:
            data = {}

        data[degree] = {
            "username": username,
            "password": self.encrypt_password(password),
            "student_number": student_number
        }

        with open(PROFILE_FILE, "w") as file:
            json.dump(data, file)

    def load_profile(self):
        degree = self.degree_var.get()
        if os.path.exists(PROFILE_FILE):
            with open(PROFILE_FILE, "r") as file:
                data = json.load(file)
                if degree in data:
                    self.entry_username.delete(0, tk.END)
                    self.entry_username.insert(0, data[degree].get("username", ""))
                    self.entry_student_number.delete(0, tk.END)
                    self.entry_student_number.insert(0, data[degree].get("student_number", ""))
                    
                    # Decrypt and insert password
                    encrypted_password = data[degree].get("password", "")
                    if encrypted_password:
                        self.entry_password.delete(0, tk.END)
                        self.entry_password.insert(0, self.decrypt_password(encrypted_password))

    def start_script(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        student_number = self.entry_student_number.get()
        degree = self.degree_var.get()
        
        if self.remember_var.get():
            self.save_profile(username, password, student_number, degree)

        self.run_selenium_script(username, password, student_number, degree)
    
    def run_selenium_script(self, username, password, student_number, degree):
        driver = webdriver.Chrome()
        driver.get("https://accounts.aut.ac.ir/cas/login")
        driver.maximize_window()

        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, "fm1"))
        )
        
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "waves-button-input").click()
        time.sleep(2)
        
        driver.switch_to.new_window()
        driver.get('https://portal.aut.ac.ir/aportal/')

        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.CLASS_NAME, "loglargbuttonG"))
        )
        driver.find_element(By.CLASS_NAME, "loglargbuttonG").click()
        WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, "loginlist"))
        )

        if degree == 'B.Sc':
             degree = 'کارشناسي'

        elif degree == 'M.Sc':
            degree = 'کارشناسي ارشد'
            
        else:
            degree = 'ٔدکتري'   


        xpath_text = f"دانشجو ({degree}-{student_number})"
        driver.find_element(By.XPATH, f"//span[contains(text(),'{xpath_text}')]").click()
    
        
        def check_driver_status(self):
            if self.driver is None or not hasattr(self.driver, "service") or not self.driver.service.is_connectable():
             self.quit()
            else:
                self.after(1, self.check_driver_status)


if __name__ == "__main__":
    app = StudentPortalApp()
    app.mainloop()