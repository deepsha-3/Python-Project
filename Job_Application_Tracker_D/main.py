import tkinter as tk
from tkinter import messagebox
from auth import AuthenticationManager, AnimatedAuthWindow
from gui import JobApplicationTracker

class MainApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.auth_manager = AuthenticationManager()
        self.current_user = None
        
        self.show_auth_window()
        
    def show_auth_window(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create animated auth window
        self.auth_window = AnimatedAuthWindow(self.root, self.auth_manager, self.on_login_success)
        
    def on_login_success(self, email):
        self.current_user = email
        self.show_main_app()
        
    def show_main_app(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create main application
        self.main_app = JobApplicationTracker(self.root, self.current_user)
        
        # Add logout button to main app
        logout_button = tk.Button(self.root, text="Logout", command=self.logout, 
                                 font=("Arial", 10), bg="#4682B4", fg="white")
        logout_button.pack(side=tk.BOTTOM, pady=10)
        
        # Add change password button
        change_pass_button = tk.Button(self.root, text="Change Password", command=self.change_password,
                                      font=("Arial", 10), bg="#4682B4", fg="white")
        change_pass_button.pack(side=tk.BOTTOM, pady=5)
        
    def change_password(self):
        # Create change password dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Change Password")
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
        tk.Label(dialog, text="Change Your Password", font=("Arial", 16, "bold")).pack(pady=20)
        
        tk.Label(dialog, text="Current Password:").pack(pady=5)
        current_password_var = tk.StringVar()
        tk.Entry(dialog, textvariable=current_password_var, show="•", width=30).pack(pady=5)
        
        tk.Label(dialog, text="New Password:").pack(pady=5)
        new_password_var = tk.StringVar()
        tk.Entry(dialog, textvariable=new_password_var, show="•", width=30).pack(pady=5)
        
        tk.Label(dialog, text="Confirm New Password:").pack(pady=5)
        confirm_password_var = tk.StringVar()
        tk.Entry(dialog, textvariable=confirm_password_var, show="•", width=30).pack(pady=5)
        
        def change_pass():
            current_password = current_password_var.get()
            new_password = new_password_var.get()
            confirm_password = confirm_password_var.get()
            
            if not current_password or not new_password:
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            if new_password != confirm_password:
                messagebox.showerror("Error", "New passwords do not match")
                return
            
            success, message = self.auth_manager.change_password(self.current_user, current_password, new_password)
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)
        
        tk.Button(dialog, text="Change Password", command=change_pass).pack(pady=20)
        
    def logout(self):
        self.current_user = None
        self.show_auth_window()
        
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run()