# gui_app.py
import tkinter as tk
from tkinter import messagebox # For pop-up messages
import database # Our database module

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("My To-Do List")
        master.geometry("600x500") # Set initial window size
        master.resizable(False, False) # Prevent resizing for simplicity

        # Ensure the database table exists
        database.create_table()

        # --- Widgets ---

        # 1. Task Input
        self.task_label = tk.Label(master, text="New Task:")
        self.task_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.task_entry = tk.Entry(master, width=40)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task_gui)
        self.add_button.grid(row=0, column=2, padx=10, pady=10)

        # 2. Task Listbox
        self.task_list_frame = tk.Frame(master)
        self.task_list_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

        self.task_listbox = tk.Listbox(self.task_list_frame, height=15, width=70, font=("Arial", 10))
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.task_list_frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # 3. Action Buttons (Mark, Delete)
        self.action_buttons_frame = tk.Frame(master)
        self.action_buttons_frame.grid(row=2, column=0, columnspan=3, pady=5)

        self.mark_complete_button = tk.Button(self.action_buttons_frame, text="Mark Complete", command=lambda: self.update_task_status_gui('completed'))
        self.mark_complete_button.pack(side=tk.LEFT, padx=5)

        self.mark_pending_button = tk.Button(self.action_buttons_frame, text="Mark Pending", command=lambda: self.update_task_status_gui('pending'))
        self.mark_pending_button.pack(side=tk.LEFT, padx=5)

        self.delete_button = tk.Button(self.action_buttons_frame, text="Delete Task", command=self.delete_task_gui)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # 4. Filter Buttons
        self.filter_buttons_frame = tk.Frame(master)
        self.filter_buttons_frame.grid(row=3, column=0, columnspan=3, pady=5)

        self.view_all_button = tk.Button(self.filter_buttons_frame, text="View All Tasks", command=lambda: self.refresh_tasks('all'))
        self.view_all_button.pack(side=tk.LEFT, padx=5)

        self.view_pending_button = tk.Button(self.filter_buttons_frame, text="View Pending", command=lambda: self.refresh_tasks('pending'))
        self.view_pending_button.pack(side=tk.LEFT, padx=5)

        self.view_completed_button = tk.Button(self.filter_buttons_frame, text="View Completed", command=lambda: self.refresh_tasks('completed'))
        self.view_completed_button.pack(side=tk.LEFT, padx=5)

        # Configure grid row and column weights for responsiveness (even though window is fixed)
        master.grid_rowconfigure(1, weight=1) # Listbox row expands vertically
        master.grid_columnconfigure(1, weight=1) # Entry field expands horizontally

        # Initial load of tasks
        self.refresh_tasks()

    def refresh_tasks(self, status_filter='all'):
        """Fetches tasks from DB and updates the Listbox."""
        self.task_listbox.delete(0, tk.END) # Clear existing items

        if status_filter == 'all':
            tasks = database.get_tasks()
        else:
            tasks = database.get_tasks(status=status_filter)

        if not tasks:
            self.task_listbox.insert(tk.END, "No tasks to display.")
            return

        for task in tasks:
            # We'll embed the ID in a hidden way for easy retrieval
            # Format: "ID. Status - Description (Created Date)"
            display_text = f"{task['status'].upper()} - {task['description']} (Added: {task['created_at'].split(' ')[0]})"
            self.task_listbox.insert(tk.END, display_text)
            # Store the task ID with the item using a dictionary or list,
            # for more direct access later when an item is selected.
            # A common way for Listbox is to use self.task_listbox.bind()
            # or retrieve the exact text and parse the ID.
            # For simplicity, we'll parse the ID from the selected string later.
            # A more robust solution might involve a mapping dictionary.

        # Store tasks for easy ID lookup (important for actions)
        self.current_tasks_data = {i: task['id'] for i, task in enumerate(tasks)}


    def get_selected_task_id(self):
        """Helper to get the ID of the selected task."""
        selected_indices = self.task_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Selection Error", "Please select a task from the list.")
            return None
        
        # Get the actual index (first selected item if multiple selected)
        selected_index = selected_indices[0]
        
        # Retrieve the task ID using the stored mapping
        task_id = self.current_tasks_data.get(selected_index)

        if task_id is None:
            messagebox.showerror("Error", "Could not retrieve task ID. Please re-select.")
            return None
        return task_id

    def add_task_gui(self):
        """Handles adding a task from GUI input."""
        description = self.task_entry.get().strip()
        if description:
            database.add_task(description)
            self.task_entry.delete(0, tk.END) # Clear the input field
            self.refresh_tasks() # Refresh the listbox
        else:
            messagebox.showwarning("Input Error", "Task description cannot be empty!")

    def update_task_status_gui(self, new_status):
        """Handles updating task status from GUI button click."""
        task_id = self.get_selected_task_id()
        if task_id is not None:
            database.update_task_status(task_id, new_status)
            self.refresh_tasks() # Refresh the listbox

    def delete_task_gui(self):
        """Handles deleting a task from GUI button click."""
        task_id = self.get_selected_task_id()
        if task_id is not None:
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                database.delete_task(task_id)
                self.refresh_tasks() # Refresh the listbox


# --- Main Application Execution ---
if __name__ == "__main__":
    root = tk.Tk() # Create the main window
    app = TodoApp(root) # Create an instance of our TodoApp
    root.mainloop() # Start the Tkinter event loop
