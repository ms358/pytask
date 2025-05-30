# main.py
import database # Import our database functions

def display_tasks(tasks):
    """Prints a formatted list of tasks."""
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n--- Your Tasks ---")
    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created: {task['created_at']}")
    print("------------------\n")

def main_menu():
    """Displays the main menu options."""
    print("1. Add New Task")
    print("2. View All Tasks")
    print("3. View Pending Tasks")
    print("4. View Completed Tasks")
    print("5. Mark Task as Complete")
    print("6. Mark Task as Pending")
    print("7. Delete Task")
    print("8. Exit")

def run_app():
    """Main function to run the To-Do List application."""
    database.create_table() # Ensure the table exists when the app starts

    while True:
        main_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            description = input("Enter task description: ")
            if description:
                database.add_task(description)
            else:
                print("Description cannot be empty.")
        elif choice == '2':
            tasks = database.get_tasks()
            display_tasks(tasks)
        elif choice == '3':
            tasks = database.get_tasks(status='pending')
            display_tasks(tasks)
        elif choice == '4':
            tasks = database.get_tasks(status='completed')
            display_tasks(tasks)
        elif choice == '5':
            try:
                task_id = int(input("Enter Task ID to mark as COMPLETE: "))
                database.update_task_status(task_id, 'completed')
            except ValueError:
                print("Invalid input. Please enter a number for Task ID.")
        elif choice == '6':
            try:
                task_id = int(input("Enter Task ID to mark as PENDING: "))
                database.update_task_status(task_id, 'pending')
            except ValueError:
                print("Invalid input. Please enter a number for Task ID.")
        elif choice == '7':
            try:
                task_id = int(input("Enter Task ID to DELETE: "))
                database.delete_task(task_id)
            except ValueError:
                print("Invalid input. Please enter a number for Task ID.")
        elif choice == '8':
            print("Exiting To-Do App. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    run_app()
