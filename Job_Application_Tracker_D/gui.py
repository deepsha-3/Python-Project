import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime, timedelta
from models import JobApplication
from database import DatabaseManager
from export import ExportManager

class JobApplicationTracker:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"Job Application Tracker - {username}")
        self.root.geometry("1000x600")
        
        self.db = DatabaseManager(username=username)
        self.export_manager = ExportManager()
        
        self.setup_ui()
        self.load_applications()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(search_frame, text="Filter by Status:").pack(side=tk.LEFT, padx=(0, 5))
        self.status_filter_var = tk.StringVar(value="All")
        status_combo = ttk.Combobox(search_frame, textvariable=self.status_filter_var, 
                                   values=["All", "Applied", "Interview", "Offer", "Rejected", "No Response"])
        status_combo.pack(side=tk.LEFT, padx=(0, 10))
        status_combo.bind('<<ComboboxSelected>>', self.on_filter)
        
        ttk.Button(search_frame, text="Upcoming Deadlines", 
                  command=self.show_upcoming_deadlines).pack(side=tk.LEFT, padx=(10, 0))
        
        # Applications treeview with scrollbar
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Company", "Role", "Status", "Deadline", "Notes")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        
        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.W)
        
        self.tree.column("ID", width=50)
        self.tree.column("Company", width=150)
        self.tree.column("Role", width=150)
        self.tree.column("Status", width=100)
        self.tree.column("Deadline", width=100)
        self.tree.column("Notes", width=300)
        
        # Scrollbar for treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind double click to edit
        self.tree.bind("<Double-1>", self.on_double_click)
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="Add Application", command=self.add_application).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Edit Application", command=self.edit_application).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Delete Application", command=self.delete_application).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT)
    
    def load_applications(self, applications=None):
        if applications is None:
            applications = self.db.get_all_applications()
        
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add applications to treeview
        for app in applications:
            self.tree.insert("", "end", values=(
                app["id"],
                app["company"],
                app["role"],
                app["status"],
                app["deadline"] or "",
                app["notes"] or ""
            ))
    
    def on_search(self, *args):
        search_term = self.search_var.get().lower()
        if not search_term:
            self.load_applications()
            return
        
        filtered_apps = self.db.search_applications(search_term)
        self.load_applications(filtered_apps)
    
    def on_filter(self, event=None):
        status = self.status_filter_var.get()
        if status == "All":
            self.load_applications()
        else:
            filtered_apps = self.db.get_applications_by_status(status)
            self.load_applications(filtered_apps)
    
    def show_upcoming_deadlines(self):
        upcoming = self.db.get_upcoming_deadlines(7)  # Next 7 days
        if not upcoming:
            messagebox.showinfo("Upcoming Deadlines", "No upcoming deadlines in the next 7 days.")
        else:
            self.load_applications(upcoming)
    
    def add_application(self):
        self.open_application_form()
    
    def edit_application(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an application to edit.")
            return
        
        item = self.tree.item(selected[0])
        app_id = item["values"][0]
        self.open_application_form(app_id)
    
    def on_double_click(self, event):
        self.edit_application()
    
    def delete_application(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an application to delete.")
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this application?"):
            item = self.tree.item(selected[0])
            app_id = item["values"][0]
            self.db.delete_application(app_id)
            self.load_applications()
    
    def open_application_form(self, app_id=None):
        form = ApplicationForm(self.root, self.db, app_id)
        self.root.wait_window(form.top)
        self.load_applications()
    
    def export_to_csv(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            applications = self.db.get_all_applications()
            self.export_manager.to_csv(applications, filename)
            messagebox.showinfo("Export Successful", f"Applications exported to {filename}")

class ApplicationForm:
    def __init__(self, parent, db, app_id=None):
        self.db = db
        self.app_id = app_id
        self.app_data = None
        
        if app_id:
            # Get existing application data
            all_apps = self.db.get_all_applications()
            for app in all_apps:
                if app["id"] == app_id:
                    self.app_data = app
                    break
        
        self.top = tk.Toplevel(parent)
        self.top.title("Edit Application" if app_id else "Add Application")
        self.top.geometry("400x300")
        self.top.transient(parent)
        self.top.grab_set()
        
        self.create_widgets()
        if self.app_data:
            self.load_data()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.top, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Company
        ttk.Label(main_frame, text="Company:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.company_var = tk.StringVar()
        company_entry = ttk.Entry(main_frame, textvariable=self.company_var, width=30)
        company_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Role
        ttk.Label(main_frame, text="Role:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.role_var = tk.StringVar()
        role_entry = ttk.Entry(main_frame, textvariable=self.role_var, width=30)
        role_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Status
        ttk.Label(main_frame, text="Status:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.status_var = tk.StringVar(value="Applied")
        status_combo = ttk.Combobox(main_frame, textvariable=self.status_var, 
                                   values=["Applied", "Interview", "Offer", "Rejected", "No Response"])
        status_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Deadline
        ttk.Label(main_frame, text="Deadline:").grid(row=3, column=0, sticky=tk.W, pady=5)
        deadline_frame = ttk.Frame(main_frame)
        deadline_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        self.deadline_var = tk.StringVar()
        deadline_entry = ttk.Entry(deadline_frame, textvariable=self.deadline_var, width=15)
        deadline_entry.pack(side=tk.LEFT)
        ttk.Button(deadline_frame, text="Today", command=self.set_today).pack(side=tk.LEFT, padx=(5, 0))
        ttk.Button(deadline_frame, text="Clear", command=self.clear_deadline).pack(side=tk.LEFT, padx=(5, 0))
        
        # Notes
        ttk.Label(main_frame, text="Notes:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        self.notes_text = tk.Text(main_frame, width=30, height=6)
        self.notes_text.grid(row=4, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(5, 0))
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Save", command=self.save).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.top.destroy).pack(side=tk.LEFT)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
    
    def load_data(self):
        if self.app_data:
            self.company_var.set(self.app_data["company"])
            self.role_var.set(self.app_data["role"])
            self.status_var.set(self.app_data["status"])
            self.deadline_var.set(self.app_data["deadline"] or "")
            self.notes_text.delete(1.0, tk.END)
            self.notes_text.insert(1.0, self.app_data["notes"] or "")
    
    def set_today(self):
        self.deadline_var.set(datetime.now().strftime("%Y-%m-%d"))
    
    def clear_deadline(self):
        self.deadline_var.set("")
    
    def save(self):
        company = self.company_var.get().strip()
        role = self.role_var.get().strip()
        
        if not company or not role:
            messagebox.showerror("Error", "Company and Role are required fields.")
            return
        
        deadline = self.deadline_var.get().strip()
        if deadline:
            # Validate date format
            try:
                datetime.strptime(deadline, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Deadline must be in YYYY-MM-DD format or empty.")
                return
        
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        application = JobApplication(
            id=self.app_id,
            company=company,
            role=role,
            status=self.status_var.get(),
            deadline=deadline or None,
            notes=notes
        )
        
        if self.app_id:
            self.db.update_application(application)
        else:
            self.db.add_application(application)
        
        self.top.destroy()