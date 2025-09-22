import hashlib
import os
import sqlite3
import re
import tkinter as tk
from tkinter import messagebox, ttk
import secrets
import string
import math
import time

class AuthenticationManager:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    salt TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS password_resets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    token TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP DEFAULT (DATETIME('now', '+1 hour'))
                )
            ''')
            conn.commit()
    
    def hash_password(self, password, salt=None):
        if salt is None:
            salt = os.urandom(32)
        password_hash = hashlib.pbkdf2_hmac(
            'sha256', password.encode('utf-8'), salt, 100000
        )
        return password_hash, salt
    
    def register_user(self, username, email, password):

        # Check if username already exists
        if self.user_exists(username):
            return False, "Username already exists"
        
        # Check if email already exists
        if self.email_exists(email):
            return False, "Email already registered"
        
        # Validate email format
        if not self.is_valid_email(email):
            return False, "Invalid email format"
        
        # Validate password strength
        if not self.is_strong_password(password):
            return False, "Password must be at least 8 characters with uppercase, lowercase, number, and special character"
        
        # Hash the password
        password_hash, salt = self.hash_password(password)
        
        # Store user in database
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, email, password_hash, salt) VALUES (?, ?, ?, ?)',
                (username, email, password_hash.hex(), salt.hex())
            )
            conn.commit()
        
        return True, "User registered successfully"
    
    def verify_user(self, email, password):
        # Get user data from database
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT password_hash, salt FROM users WHERE email = ?',
                (email,)
            )
            result = cursor.fetchone()
        
        if not result:
            return False, "User not found"
        
        stored_hash_hex, salt_hex = result
        stored_hash = bytes.fromhex(stored_hash_hex)
        salt = bytes.fromhex(salt_hex)
        
        # Hash the provided password with the stored salt
        provided_hash, _ = self.hash_password(password, salt)
        
        # Compare the hashes
        if provided_hash == stored_hash:
            return True, "Login successful"
        else:
            return False, "Invalid password"
    
    def user_exists(self, username):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id FROM users WHERE username = ?',
                (username,)
            )
            return cursor.fetchone() is not None
    
    def email_exists(self, email):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id FROM users WHERE email = ?',
                (email,)
            )
            return cursor.fetchone() is not None
    
    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_strong_password(self, password):
        if len(password) < 8:
            return False
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'[0-9]', password):
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        return True
    
    def generate_reset_token(self):
        return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
    
    def initiate_password_reset(self, email):
        if not self.email_exists(email):
            return False, "Email not registered"
        
        token = self.generate_reset_token()
        
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Remove any existing tokens for this email
            cursor.execute('DELETE FROM password_resets WHERE email = ?', (email,))
            # Insert new token
            cursor.execute(
                'INSERT INTO password_resets (email, token) VALUES (?, ?)',
                (email, token)
            )
            conn.commit()
        
        # In a real application, you would send an email here
        # For demonstration, we'll just show the token in a messagebox
        messagebox.showinfo("Password Reset", f"Reset token: {token}\n\nIn a real application, this would be sent via email.")
        
        return True, "Password reset initiated"
    
    def reset_password(self, email, token, new_password):
        # Validate token
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT * FROM password_resets WHERE email = ? AND token = ? AND expires_at > datetime("now")',
                (email, token)
            )
            result = cursor.fetchone()
            
            if not result:
                return False, "Invalid or expired token"
            
            # Validate password strength
            if not self.is_strong_password(new_password):
                return False, "Password must be at least 8 characters with uppercase, lowercase, number, and special character"
            
            # Update password
            password_hash, salt = self.hash_password(new_password)
            cursor.execute(
                'UPDATE users SET password_hash = ?, salt = ? WHERE email = ?',
                (password_hash.hex(), salt.hex(), email)
            )
            
            # Remove used token
            cursor.execute('DELETE FROM password_resets WHERE email = ?', (email,))
            conn.commit()
        
        return True, "Password reset successful"
    
    def change_password(self, email, current_password, new_password):
        # Verify current password
        success, message = self.verify_user(email, current_password)
        if not success:
            return False, message
        
        # Validate password strength
        if not self.is_strong_password(new_password):
            return False, "Password must be at least 8 characters with uppercase, lowercase, number, and special character"
        
        # Update password
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            password_hash, salt = self.hash_password(new_password)
            cursor.execute(
                'UPDATE users SET password_hash = ?, salt = ? WHERE email = ?',
                (password_hash.hex(), salt.hex(), email)
            )
            conn.commit()
        
        return True, "Password changed successfully"


class AnimatedAuthWindow:
    def __init__(self, root, auth_manager, on_login_success):
        self.root = root
        self.auth_manager = auth_manager
        self.on_login_success = on_login_success
        
        # Center the window on screen
        self.center_window(1000, 600)
        
        # Animation variables
        self.animation_running = False
        self.current_hue = 0
        self.canvas = None
        
        self.setup_ui()
        
        # Start background animation
        self.animate_background()
    
    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(False, False)
    
    def setup_ui(self):
        self.root.title("Job Application Tracker")
        self.root.configure(bg="#2c3e50")
        
        # Create canvas for animated background
        self.canvas = tk.Canvas(self.root, bg="#2c3e50", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Main container
        self.main_container = tk.Frame(self.canvas, bg="#2c3e50")
        self.main_container.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=800, height=500)
        
        # Create the animated panels
        self.create_panels()
        
        # Start with login form
        self.show_login_form()
    
    def create_panels(self):
        # Login form - initially visible
        self.login_frame = tk.Frame(self.main_container, bg="white", relief=tk.FLAT, bd=0)
        self.login_frame.place(relx=0, rely=0, relwidth=0.5, relheight=1)
        
        # Welcome panel - initially on the right side
        self.welcome_frame = tk.Frame(self.main_container, bg="#3498db", relief=tk.FLAT, bd=0)
        self.welcome_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)
        
        # Create login form content
        self.create_login_form()
        
        # Create welcome panel content
        self.create_welcome_panel()
    
    def create_login_form(self):
        # Title
        title_label = tk.Label(self.login_frame, text="Welcome Back!", font=("Arial", 24, "bold"), 
                              bg="white", fg="#2c3e50")
        title_label.pack(pady=(40, 10))
        
        subtitle_label = tk.Label(self.login_frame, text="Enter your personal details to use all of site features", 
                                 font=("Arial", 10), bg="white", fg="#7f8c8d")
        subtitle_label.pack(pady=(0, 40))
        
        # Email field
        email_frame = tk.Frame(self.login_frame, bg="white")
        email_frame.pack(pady=10, padx=40, fill=tk.X)
        
        tk.Label(email_frame, text="Email", font=("Arial", 10, "bold"), 
                bg="white", fg="#34495e").pack(anchor="w")
        
        self.login_email_var = tk.StringVar()
        email_entry = tk.Entry(email_frame, textvariable=self.login_email_var, 
                              font=("Arial", 12), bd=1, relief=tk.SOLID, highlightthickness=1,
                              highlightcolor="#3498db", highlightbackground="#ecf0f1")
        email_entry.pack(pady=5, fill=tk.X)
        
        # Password field
        password_frame = tk.Frame(self.login_frame, bg="white")
        password_frame.pack(pady=10, padx=40, fill=tk.X)
        
        tk.Label(password_frame, text="Password", font=("Arial", 10, "bold"), 
                bg="white", fg="#34495e").pack(anchor="w")
        
        self.login_password_var = tk.StringVar()
        password_entry = tk.Entry(password_frame, textvariable=self.login_password_var, 
                                 font=("Arial", 12), show="•", bd=1, relief=tk.SOLID,
                                 highlightthickness=1, highlightcolor="#3498db", highlightbackground="#ecf0f1")
        password_entry.pack(pady=5, fill=tk.X)
        
        # Forgot password
        forgot_frame = tk.Frame(self.login_frame, bg="white")
        forgot_frame.pack(pady=5, padx=40, fill=tk.X)
        
        tk.Button(forgot_frame, text="Forgot Your Password?", font=("Arial", 9), 
                 bg="white", fg="#3498db", bd=0, cursor="hand2",
                 command=self.show_forgot_password).pack(anchor="e")
        
        # Login button
        login_btn = tk.Button(self.login_frame, text="SIGN IN", font=("Arial", 12, "bold"), 
                             bg="#3498db", fg="white", width=20, height=2, bd=0,
                             cursor="hand2", command=self.login)
        login_btn.pack(pady=20)
        
        # Register prompt
        register_prompt = tk.Frame(self.login_frame, bg="white")
        register_prompt.pack(pady=10)
        
        tk.Label(register_prompt, text="Don't have an account?", font=("Arial", 9), 
                bg="white", fg="#7f8c8d").pack(side=tk.LEFT)
        
        tk.Button(register_prompt, text="Sign Up", font=("Arial", 9, "bold"), 
                 bg="white", fg="#3498db", bd=0, cursor="hand2",
                 command=self.show_register_form).pack(side=tk.LEFT, padx=5)
    
    def create_welcome_panel(self):
        # Title
        title_label = tk.Label(self.welcome_frame, text="Hello, Friend!", font=("Arial", 24, "bold"), 
                              bg="#3498db", fg="white")
        title_label.pack(pady=(120, 10))
        
        subtitle_label = tk.Label(self.welcome_frame, text="Register with your personal details to use all of site features", 
                                 font=("Arial", 10), bg="#3498db", fg="white")
        subtitle_label.pack(pady=(0, 30))
        
        # Register button
        register_btn = tk.Button(self.welcome_frame, text="SIGN UP", font=("Arial", 12, "bold"), 
                                bg="white", fg="#3498db", width=20, height=2, bd=0,
                                cursor="hand2", command=self.show_register_form)
        register_btn.pack(pady=20)
    
    def show_login_form(self):
        self.animate_panels(0)
        self.root.title("Job Application Tracker - Sign In")
    
    def show_register_form(self):
        # First animate the panels to the left
        self.animate_panels(-0.5)
        
        # Then create the register form on the right side
        if hasattr(self, 'register_frame'):
            self.register_frame.destroy()
        
        self.register_frame = tk.Frame(self.main_container, bg="white", relief=tk.FLAT, bd=0)
        self.register_frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)
        
        # Create register form content
        self.create_register_form_content()
        
        self.root.title("Job Application Tracker - Sign Up")
    
    def create_register_form_content(self):
        # Title
        title_label = tk.Label(self.register_frame, text="Create Account", font=("Arial", 24, "bold"), 
                              bg="white", fg="#2c3e50")
        title_label.pack(pady=(40, 10))
        
        subtitle_label = tk.Label(self.register_frame, text="or use your email for registration", 
                                 font=("Arial", 10), bg="white", fg="#7f8c8d")
        subtitle_label.pack(pady=(0, 40))
        
        # Name field
        name_frame = tk.Frame(self.register_frame, bg="white")
        name_frame.pack(pady=10, padx=40, fill=tk.X)
        
        tk.Label(name_frame, text="Name", font=("Arial", 10, "bold"), 
                bg="white", fg="#34495e").pack(anchor="w")
        
        self.register_name_var = tk.StringVar()
        name_entry = tk.Entry(name_frame, textvariable=self.register_name_var, 
                             font=("Arial", 12), bd=1, relief=tk.SOLID, highlightthickness=1,
                             highlightcolor="#3498db", highlightbackground="#ecf0f1")
        name_entry.pack(pady=5, fill=tk.X)
        
        # Email field
        email_frame = tk.Frame(self.register_frame, bg="white")
        email_frame.pack(pady=10, padx=40, fill=tk.X)
        
        tk.Label(email_frame, text="Email", font=("Arial", 10, "bold"), 
                bg="white", fg="#34495e").pack(anchor="w")
        
        self.register_email_var = tk.StringVar()
        email_entry = tk.Entry(email_frame, textvariable=self.register_email_var, 
                              font=("Arial", 12), bd=1, relief=tk.SOLID, highlightthickness=1,
                              highlightcolor="#3498db", highlightbackground="#ecf0f1")
        email_entry.pack(pady=5, fill=tk.X)
        
        # Password field
        password_frame = tk.Frame(self.register_frame, bg="white")
        password_frame.pack(pady=10, padx=40, fill=tk.X)
        
        tk.Label(password_frame, text="Password", font=("Arial", 10, "bold"), 
                bg="white", fg="#34495e").pack(anchor="w")
        
        self.register_password_var = tk.StringVar()
        password_entry = tk.Entry(password_frame, textvariable=self.register_password_var, 
                                 font=("Arial", 12), show="•", bd=1, relief=tk.SOLID,
                                 highlightthickness=1, highlightcolor="#3498db", highlightbackground="#ecf0f1")
        password_entry.pack(pady=5, fill=tk.X)
        
        # Register button
        register_btn = tk.Button(self.register_frame, text="SIGN UP", font=("Arial", 12, "bold"), 
                                bg="#3498db", fg="white", width=20, height=2, bd=0,
                                cursor="hand2", command=self.register)
        register_btn.pack(pady=20)
        
        # Login prompt
        login_prompt = tk.Frame(self.register_frame, bg="white")
        login_prompt.pack(pady=10)
        
        tk.Label(login_prompt, text="Already have an account?", font=("Arial", 9), 
                bg="white", fg="#7f8c8d").pack(side=tk.LEFT)
        
        tk.Button(login_prompt, text="Sign In", font=("Arial", 9, "bold"), 
                 bg="white", fg="#3498db", bd=0, cursor="hand2",
                 command=self.show_login_form).pack(side=tk.LEFT, padx=5)
    
    def animate_panels(self, target_relx):
        if self.animation_running:
            return
            
        self.animation_running = True
        current_relx = float(self.login_frame.place_info()["relx"])
        
        # Calculate step
        step = (target_relx - current_relx) / 15
        
        def move():
            nonlocal current_relx
            current_relx += step
            
            if (step > 0 and current_relx >= target_relx) or (step < 0 and current_relx <= target_relx):
                current_relx = target_relx
                self.login_frame.place(relx=current_relx, rely=0, relwidth=0.5, relheight=1)
                self.welcome_frame.place(relx=current_relx + 0.5, rely=0, relwidth=0.5, relheight=1)
                self.animation_running = False
                return
            
            self.login_frame.place(relx=current_relx, rely=0, relwidth=0.5, relheight=1)
            self.welcome_frame.place(relx=current_relx + 0.5, rely=0, relwidth=0.5, relheight=1)
            self.root.after(20, move)
        
        move()
    
    def animate_background(self):
        # Create a smooth color changing background
        self.current_hue = (self.current_hue + 0.5) % 360
        r, g, b = self.hsv_to_rgb(self.current_hue, 0.3, 0.2)
        color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        
        self.canvas.configure(bg=color)
        self.main_container.configure(bg=color)
        
        # Schedule the next animation frame
        self.root.after(50, self.animate_background)
    
    def hsv_to_rgb(self, h, s, v):
        # Convert HSV to RGB color
        h = h / 360.0
        if s == 0.0:
            return v, v, v
        
        i = int(h * 6)
        f = (h * 6) - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))
        
        if i % 6 == 0:
            return v, t, p
        elif i % 6 == 1:
            return q, v, p
        elif i % 6 == 2:
            return p, v, t
        elif i % 6 == 3:
            return p, q, v
        elif i % 6 == 4:
            return t, p, v
        else:
            return v, p, q
    
    def login(self):
        email = self.login_email_var.get().strip()
        password = self.login_password_var.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password")
            return
        
        success, message = self.auth_manager.verify_user(email, password)
        if success:
            messagebox.showinfo("Success", message)
            self.root.after(1000, lambda: self.on_login_success(email))
        else:
            messagebox.showerror("Error", message)
    
    def register(self):
        username = self.register_name_var.get().strip()
        email = self.register_email_var.get().strip()
        password = self.register_password_var.get()
        
        if not username or not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        success, message = self.auth_manager.register_user(username, email, password)
        if success:
            messagebox.showinfo("Success", message)
            self.show_login_form()
        else:
            messagebox.showerror("Error", message)
    
    def show_forgot_password(self):
        # Create forgot password dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Reset Password")
        dialog.geometry("400x250")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Content
        tk.Label(dialog, text="Reset Your Password", font=("Arial", 16, "bold")).pack(pady=20)
        
        tk.Label(dialog, text="Enter your email address:").pack(pady=5)
        email_var = tk.StringVar()
        tk.Entry(dialog, textvariable=email_var, width=30).pack(pady=10)
        
        def send_reset():
            email = email_var.get().strip()
            if not email:
                messagebox.showerror("Error", "Please enter your email address")
                return
            
            success, message = self.auth_manager.initiate_password_reset(email)
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
                self.show_reset_token_dialog(email)
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(dialog, text="Send Reset Link", command=send_reset).pack(pady=20)
    
    def show_reset_token_dialog(self, email):
        # Create reset token dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Enter Reset Token")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # Content
        tk.Label(dialog, text="Enter Reset Token", font=("Arial", 16, "bold")).pack(pady=20)
        
        tk.Label(dialog, text="Token sent to your email:").pack(pady=5)
        token_var = tk.StringVar()
        tk.Entry(dialog, textvariable=token_var, width=30).pack(pady=5)
        
        tk.Label(dialog, text="New Password:").pack(pady=5)
        new_password_var = tk.StringVar()
        tk.Entry(dialog, textvariable=new_password_var, show="•", width=30).pack(pady=5)
        
        tk.Label(dialog, text="Confirm New Password:").pack(pady=5)
        confirm_password_var = tk.StringVar()
        tk.Entry(dialog, textvariable=confirm_password_var, show="•", width=30).pack(pady=5)
        
        def reset_password():
            token = token_var.get().strip()
            new_password = new_password_var.get()
            confirm_password = confirm_password_var.get()
            
            if not token or not new_password:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if new_password != confirm_password:
                messagebox.showerror("Error", "Passwords do not match")
                return
            
            success, message = self.auth_manager.reset_password(email, token, new_password)
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(dialog, text="Reset Password", command=reset_password).pack(pady=20)