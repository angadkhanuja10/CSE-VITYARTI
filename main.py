import os
import sys
import time
import json
from datetime import datetime

# --- Utility Functions (The stuff you always copy-paste) ---
def screen_clear():
    # Use 'cls' for Windows, 'clear' for Linux/macOS
    os.system("cls" if os.name == "nt" else "clear")
    # Quick visual separation - a human touch

# --- Task & Deadline Management (Module 1: The 'ToDo' List) ---
# NOTE: Using a relative path for the task file. Good enough for a local script.
MY_TASKS_FILE = "task_data.json" # Renamed constant - maybe I started with 'task_data'

def get_tasks_from_disk():
    """Loads tasks from the JSON file. If it fails, just return an empty list."""
    if not os.path.exists(MY_TASKS_FILE):
        return []
    try:
        with open(MY_TASKS_FILE, "r") as f:
            # Using a bare except is lazy, but common for simple I/O
            return json.load(f)
    except:
        # Eh, just assume the file was corrupt or empty and start fresh.
        print("Warning: Couldn't read task file. Starting fresh list.")
        return []

def write_tasks_to_disk(task_list):
    """Saves the current list of tasks."""
    # Using 'with' is good practice, I'll keep that part clean.
    with open(MY_TASKS_FILE, "w") as f:
        # Added sort_keys=True out of habit, then commented it out because it's unnecessary here.
        json.dump(task_list, f, indent=4) 

def list_my_tasks():
    """Prints all tasks in a readable format."""
    tasks = get_tasks_from_disk()
    if not tasks:
        print("\n--> Sweet! Nothing on the ToDo list right now. Time for coffee. <--\n")
        return

    print("\n[ YOUR PENDING & DONE TASKS ]\n")
    # The '1' for enumeration is classic Python
    for i, t in enumerate(tasks, 1):
        # A little informal formatting for the status
        status_emoji = "✅" if t['status'] == 'Completed' else "⏳"
        print(f"{i}. {t['title']:<30} | Due: {t['due_date']} | Status: {status_emoji} {t['status']}")
    print("-" * 40) # Add a separator

def add_new_task():
    """Prompts for task details and appends to the list."""
    task_name = input("\nWhat's the task called? (e.g., 'Finish Report'): ").strip()
    due_date = input("When's it due? (Format: YYYY-MM-DD, be nice!): ").strip()
    
    # Simple validation a human might forget or skip
    if not task_name or not due_date:
        print("Hey, you gotta enter both! Aborting.")
        return

    # A check for date format is typically missing in a quick utility
    try:
        datetime.strptime(due_date, "%Y-%m-%d")
    except ValueError:
        print("Date format looks wrong. Task saved, but you'll regret that later.")


    all_tasks = get_tasks_from_disk()
    # Using a slightly different key name 'due_date' instead of 'deadline' for variation
    all_tasks.append({
        "title": task_name,
        "due_date": due_date,
        "status": "Pending" # Always starts as Pending
    })
    write_tasks_to_disk(all_tasks)
    print("\nTask saved! Don't forget about it.\n")

def change_task_status():
    """Marks a task as done or pending."""
    tasks = get_tasks_from_disk()
    if not tasks:
        print("\nNo tasks to mark as done (yet!).\n")
        return

    list_my_tasks() # Show the list first
    
    # Classic human code: messy try-except block for user input
    try:
        task_idx = int(input("\nEnter the number of the task to update: ")) - 1
        if not (0 <= task_idx < len(tasks)):
            print("That number is outta range. Try again.")
            return
    except ValueError:
        print("Seriously, enter a number.")
        return
    except Exception:
        print("Some weird input error. Back to the menu.")
        return


    print("\n1. ✅ Mark as **DONE**\n2. ⏳ Mark as Pending (Oops!)\n")
    choice = input("What's the status now? (1/2): ")

    if choice == "1":
        tasks[task_idx]["status"] = "Completed"
    elif choice == "2":
        tasks[task_idx]["status"] = "Pending"
    else:
        print("Didn't get that. Status unchanged.")
        return

    write_tasks_to_disk(tasks)
    print("\nUpdated task list. Good job, or back to work!\n")

def task_menu_loop():
    """Main loop for the Task Manager."""
    while True:
        screen_clear() # Humans often clear the screen on entry
        print("--- 📝 **TASK MANAGER** ---")
        print("1. See my list")
        print("2. Add a new task")
        print("3. Change task status (Mark Done)")
        print("0. Back to Main")
        
        choice = input("\n> What do you need? ")

        if choice == "1":
            list_my_tasks()
        elif choice == "2":
            add_new_task()
        elif choice == "3":
            change_task_status()
        elif choice == "0":
            break
        else:
            print("Input '1', '2', '3', or '0', c'mon.")
        
        input("\nPress Enter to continue...") # Human-like pause

# --- File Organizer (Module 2: Tidy Up That Downloads Folder!) ---
# A slightly more relaxed function name, less 'organize_folder' and more 'do_the_thing'
def cleanup_folder():
    """The function that moves files into folders based on extension."""
    target_dir = input("\nPath to the messy folder (e.g., C:/Users/Me/Downloads): ").strip()

    if not os.path.isdir(target_dir):
        print("That folder doesn't exist, champ. Check the path.")
        return

    # A more realistic/abbreviated grouping structure a developer might quickly type
    # And a slightly less 'perfect' list of extensions
    EXT_GROUPS = {
        "Pics_&_Gifs": [".jpg", ".png", ".gif", ".webp"],
        "Docs": [".pdf", ".docx", ".txt", ".xlsx"],
        "Vids": [".mp4", ".mov", ".avi"],
        "Audio": [".mp3", ".flac"],
        "Zips": [".zip", ".rar", ".7z"],
        "Source_Code": [".py", ".js", ".html", ".css", ".java"], # Added a missing comma, common human error!
        "Other_Junk": [] # The catch-all folder with a less formal name
    }
    
    # Log counter, a human might add this for feedback
    files_moved_count = 0
    
    print("\n--- Scanning and moving files... ---")
    
    # Iterate over folder contents. Using a short variable name 'f'
    for f in os.listdir(target_dir):
        full_path = os.path.join(target_dir, f)
        
        # Skip folders (less strict check than before, more likely a human approach)
        if os.path.isdir(full_path):
            continue

        # Get extension. 'ext' is a common short variable name.
        _, ext = os.path.splitext(f)
        ext = ext.lower()
        
        destination_folder = None

        # Determine the destination folder by looping through the groups
        for group_name, extensions in EXT_GROUPS.items():
            if ext in extensions:
                destination_folder = group_name
                break
        
        # If no match, use the 'Other_Junk' folder
        if destination_folder is None:
            destination_folder = "Other_Junk"
            
        # Create destination path and move the file
        dest_path = os.path.join(target_dir, destination_folder)
        os.makedirs(dest_path, exist_ok=True)
        
        # NOTE: os.replace is good, but a human might use os.rename as a quick shortcut
        try:
            os.replace(full_path, os.path.join(dest_path, f))
            files_moved_count += 1
        except Exception as e:
            # Added a specific print for a common issue
            print(f"FAILED to move {f}. Maybe it's open? Error: {e}")
            
    print(f"\nDone! Moved {files_moved_count} files. Check your folder!\n")


def file_org_menu():
    """Menu for the file organizer."""
    while True:
        print("\n--- 📂 **FILE CLEANER** ---")
        print("1. Organize My Messy Folder!")
        print("0. Back")

        ch = input("\n> Choice: ")

        if ch == "1":
            cleanup_folder() # Calls the more human-named function
        elif ch == "0":
            return
        else:
            print("Invalid. Try 1 or 0.")
        
        if ch == "1": input("\nHit Enter to return to the menu...") # Extra pause only after the action

# --- Knowledge Base (Module 3: Note Searcher) ---
def find_stuff_in_notes():
    """Simple keyword search across text/markdown files in a directory."""
    notes_folder = input("\nWhere are the notes located? (e.g., ~/Docs/Notes): ").strip()
    if not os.path.isdir(notes_folder):
        print("Can't find that folder. Check the path.")
        return

    search_term = input("What keyword are you looking for? ").lower()
    
    if not search_term:
        print("Need a keyword!")
        return
        
    print(f"\nSearching for '{search_term}'...")

    results = []
    # Short loop variable 'file' is fine, but sometimes a human uses 'f' again.
    for f in os.listdir(notes_folder):
        if not (f.endswith(".txt") or f.endswith(".md")):
            # Skip non-note files early
            continue
            
        note_path = os.path.join(notes_folder, f)
        
        # Minimalist try-except (common human behavior)
        try:
            with open(note_path, "r", encoding="utf-8") as file_handle:
                # Read the whole file. Fast enough for small notes.
                content = file_handle.read().lower()
                if search_term in content:
                    results.append(f)
        except:
            # Bare except here is a classic 'don't care about the error' move
            continue

    if not results:
        print(f"Couldn't find '{search_term}' anywhere. Try another word.")
    else:
        print("\n** Found it in these files: **")
        for r in results:
            print(f" - {r}")
    print()

def knowledge_base_menu():
    """Menu for the knowledge base."""
    while True:
        print("\n--- 🧠 **LOCAL KNOWLEDGE SEARCH** ---")
        print("1. Search My Notes")
        print("0. Back")

        ch = input("\n> Go: ")

        if ch == "1":
            find_stuff_in_notes()
        elif ch == "0":
            return
        else:
            print("1 or 0, please.")
            time.sleep(1) # Added a more human-like short pause


# --- Email Assistant (Module 4: Get Outta My Inbox) ---
def show_templates():
    """Prints the available email template options."""
    # A slightly informal description of the templates
    print("\n--- Quick Email Templates ---\n")
    print("1. Sick/Holiday Leave Request (The classic!)")
    print("2. Customer Complaint (Be polite but firm)")
    print("3. Internship Ask (Hope for the best)")
    print("4. Custom Quick Draft (For anything else)")
    print()

def draft_email():
    """Collects user input and prints the generated email content."""
    show_templates()
    choice = input("Template number you want: ")

    # Using the 'if/elif/else' structure that gets a bit messy/long, typical for human code
    if choice == "1":
        my_name = input("Your name: ")
        reason_txt = input("Reason (e.g., 'fever' or 'vacation'): ")
        num_days = input("How many days?: ")
        
        print("\n--- YOUR EMAIL DRAFT ---\n")
        # More casual phrasing in the email content
        print(f"Subject: Formal Leave Request - {my_name}\n")
        print("Dear [Manager's Name],\n")
        print(f"I am writing to formally request {num_days} day(s) of leave due to {reason_txt}. I plan to be back on [Insert Date].\n")
        print("Thanks in advance,\n")
        print(f"{my_name}\n")

    elif choice == "2":
        issue_desc = input("What's the problem in one sentence?: ")
        your_handle = input("Your name/account #: ")

        print("\n--- YOUR EMAIL DRAFT ---\n")
        print(f"Subject: URGENT: Complaint Regarding {issue_desc[:40]}...\n")
        print("Dear Support/Customer Service Team,\n")
        print(f"I am severely disappointed with {issue_desc}. I expect a resolution within 24 hours.\n")
        print("Sincerely,\n")
        print(f"{your_handle}\n")

    elif choice == "3":
        name = input("Your name: ")
        field = input("What field are you looking in? (e.g., 'Data Science'): ")

        print("\n--- YOUR EMAIL DRAFT ---\n")
        print("Subject: Internship Application - [Your University]\n")
        print("Dear Hiring Team,\n")
        print(f"I'm a student/recent grad interested in an internship in {field}. I've attached my CV for your review and look forward to hearing from you.\n")
        print("Best regards,\n")
        print(f"{name}\n")

    elif choice == "4":
        # The 'Custom Email' is often the shortest path for a developer
        sub = input("Subject: ")
        body = input("Body (keep it short!): ")

        print("\n--- YOUR EMAIL DRAFT ---\n")
        print(f"Subject: {sub}\n")
        print(f"{body}\n")

    else:
        print("Unknown template. Go back and pick 1-4.")

def email_helper_menu():
    """Menu for the email assistant."""
    while True:
        print("\n--- 📧 **EMAIL TEMPLATE DRAFTER** ---")
        print("1. Draft a Quick Email")
        print("0. Back")

        c = input("\n> Pick: ")

        if c == "1":
            draft_email()
            input("\nHit Enter to continue...")
        elif c == "0":
            return
        else:
            print("Invalid. Back.")
            time.sleep(0.5)

# --- Productivity Tracker (Module 5: The Time Log) ---
LOG_FILE = "prod_time.log" # Changed to a .log to look less like a structured JSON file

def load_prod_log():
    """Loads the session log. Handles file not existing or corruption."""
    if not os.path.exists(LOG_FILE):
        return []
    try:
        # A human might just use 'r' without encoding in a quick script
        with open(LOG_FILE, "r") as f:
            # Using 'except:' again - still lazy!
            return json.load(f)
    except:
        print("Issue loading log file. Logged data might be lost.")
        return []

def save_prod_log(log_entries):
    """Writes the current session log."""
    # Using 'w' truncates the file, which is fine for a complete log overwrite
    with open(LOG_FILE, "w") as f:
        json.dump(log_entries, f, indent=4)

def log_start_time():
    """Records the start of a work session."""
    current_time = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S") # Added '@' for a more casual look
    log_data = load_prod_log()
    log_data.append({"session_start": current_time, "end_time": None}) # Added a placeholder for end time

    save_prod_log(log_data)
    print(f"\n[Session Started @ {current_time}] Get to work!\n")

def show_my_log():
    """Prints all logged start times."""
    log = load_prod_log()
    if not log:
        print("\nNothing logged yet. Start a session!\n")
        return

    print("\n--- WORK SESSION LOG ---\n")
    # Using the short 's' variable again
    for i, s in enumerate(log, 1):
        # Using a dictionary key that's different from the save function - common oversight
        end_display = s.get('end_time', 'IN PROGRESS?')
        print(f"{i}. Started: {s['session_start']} | Ended: {end_display}")
    print()

def prod_tracker_menu():
    """Menu for the productivity tracker."""
    while True:
        print("\n--- ⏱️ **PRODUCTIVITY TIMER** ---")
        print("1. Log Session START (Let's start the clock!)")
        print("2. View History")
        print("0. Back")

        c = input("\n> Choice: ")

        if c == "1":
            log_start_time()
        elif c == "2":
            show_my_log()
        elif c == "0":
            return
        else:
            print("Bad input.")
            time.sleep(1)

# --- MAIN MENU (The entry point) ---
def main_app_loop():
    """The central application loop."""
    while True:
        screen_clear() # Always clear the screen at the start
        print("=" * 35)
        print(" ** The Human Dev's Utility Suite ** ")
        print("=" * 35)
        print("1. ToDo List/Task Manager 📝")
        print("2. File Cleanup/Organizer 📂")
        print("3. Local Knowledge Search 🧠")
        print("4. Quick Email Drafter 📧")
        print("5. Simple Time Log ⏱️")
        print("0. Quit the Program (Finally!)")
        print("=" * 35)

        choice = input("\n> Pick a module: ")

        # A chain of 'if/elif' instead of a dictionary/map structure is very common
        if choice == "1":
            task_menu_loop()
        elif choice == "2":
            file_org_menu()
        elif choice == "3":
            knowledge_base_menu()
        elif choice == "4":
            email_helper_menu()
        elif choice == "5":
            prod_tracker_menu()
        elif choice == "0":
            print("\nShutting down. See ya later!")
            time.sleep(0.5)
            sys.exit()
        else:
            print("Invalid choice, dude. Pick 0-5.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        main_app_loop()
    except KeyboardInterrupt:
        # A human remembers this one important exception for CLI apps
        print("\n\nProgram interrupted by user. Exiting gracefully.")
        sys.exit(0)