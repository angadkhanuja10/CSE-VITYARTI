import os
import sys
import time
import json
from datetime import datetime
import shutil

# --- Utility Functions (The basic stuff) ---
def screen_clear():
    """Clears the console screen using OS commands."""
    os.system("cls" if os.name == "nt" else "clear")

# --- Global Constants (The stuff I set and immediately forgot about) ---
# Using a relative folder that might clutter the repo, because who cares?
APP_DATA_DIR = "./local_dev_data"

# Naming files whatever I felt like that day
TASK_FILE_NAME = "my_tasks.dat" 
LOG_FILE_NAME = "times.log"

TASK_FILE_PATH = os.path.join(APP_DATA_DIR, TASK_FILE_NAME)
LOG_FILE_PATH = os.path.join(APP_DATA_DIR, LOG_FILE_NAME)

def setup_data_dir():
    """Ensure the data directory exists."""
    # exist_ok=True means I don't have to check if it's there, nice!
    os.makedirs(APP_DATA_DIR, exist_ok=True)

# ------------------------------------------------------------------
# MODULE 1: Task Manager (The one that actually works)
# ------------------------------------------------------------------

def load_the_tasks():
    """Grabs the tasks from disk. If anything weird happens, just fail quietly."""
    setup_data_dir()
    if not os.path.exists(TASK_FILE_PATH):
        return []
    try:
        with open(TASK_FILE_PATH, "r") as f:
            # Bare except is fastest to type
            return json.load(f)
    except:
        print("!! WARNING: Task file seems bad (oops). Starting fresh. !!")
        return []

def save_task_list(tList):
    """Writes the tasks back to the disk."""
    setup_data_dir()
    # Used 'indent=2' this time, inconsistent with the other module's 'indent=4'
    with open(TASK_FILE_PATH, "w") as f:
        json.dump(tList, f, indent=2) 

def view_current_tasks():
    """Prints all tasks with a slightly different, informal format."""
    tasks = load_the_tasks()
    if not tasks:
        print("\n--> Nothing left to do! You are free! <--\n")
        return

    print("\n[ YOUR TO-DO LIST (Don't look at the due dates) ]\n")
    # Using 'i' for index again
    for i, t in enumerate(tasks, 1):
        # Using a shortened, abbreviated key 'stat' again
        status = "**DONE**" if t.get('stat') == 'Completed' else "PENDING"
        # Using dictionary access without .get() because I'm 99% sure the keys are there
        print(f"[{i:02d}] {t['title']:<35} | DUE: {t['due']} | {status}")
    print("-" * 50)

def create_new_task():
    """Add a task. Minimal validation, let the user suffer later."""
    title = input("\nTask name (keep it brief): ").strip()
    # Using an ambiguous input prompt
    due = input("Due date (e.g., tomorrow, or 2026-01-30): ").strip()

    if not title:
        print("Task needs a name. Aborting.")
        return

    taskList = load_the_tasks()
    taskList.append({
        "title": title,
        "due": due, # Storing potentially bad date format
        "stat": "Pending" # Using the abbreviated key
    })
    save_task_list(taskList)
    print("\n...Task added. It's officially on your plate.\n")

def toggle_task_status():
    """Marks a task done or pending with slightly lazy input handling."""
    tasks = load_the_tasks()
    if not tasks:
        print("\nNo tasks to mark.\n")
        return

    view_current_tasks()
    
    try:
        # Not checking for non-digit input effectively
        idx = int(input("\nTask # to flip status: ")) - 1 
        
        if 0 <= idx < len(tasks):
            # Using the abbreviated key 'stat'
            current_status = tasks[idx].get('stat', 'Pending')
            new_status = "Completed" if current_status == "Pending" else "Pending"
            tasks[idx]['stat'] = new_status
            save_task_list(tasks)
            print(f"\nTask {idx + 1} status changed to **{new_status}**.")
        else:
            print("\nThat number is outside the bounds. Read the list carefully!")
    except ValueError:
        print("\nMust be a digit. I can't work with that.")
    except Exception:
        print("\nSome random issue happened. Try again.")


def task_manager_menu():
    """The task manager menu loop."""
    while True:
        screen_clear()
        print("~" * 30)
        print(" 📝 TASK MANAGER (v1.1) ")
        print("~" * 30)
        print("1. View Tasks")
        print("2. Add Task")
        print("3. Toggle Task Status (Done/Pending)")
        print("0. Back")
        
        choice = input("\n> What now? ").strip()

        if choice == "1":
            view_current_tasks()
        elif choice == "2":
            create_new_task()
        elif choice == "3":
            toggle_task_status()
        elif choice == "0":
            break
        else:
            print("Invalid input. Try again.")
        
        input("\n...hit ENTER...")

# ------------------------------------------------------------------
# MODULE 2: File Organizer (The chaotic one)
# ------------------------------------------------------------------

def run_file_cleanup():
    """Moves files into categorized subfolders."""
    # Use a prompt that favors quick local path input
    folder_to_clean = input("\nFolder path to organize: ").strip()

    if not os.path.isdir(folder_to_clean):
        print("Folder not found or it's not a folder, sorry.")
        return

    # Inconsistent grouping names (some plural, some abbreviated, some all caps)
    FILE_GROUPINGS = {
        "PICS": [".jpg", ".jpeg", ".png", ".gif"],
        "Docs_PDFs": [".pdf", ".doc", ".docx", ".txt", ".xlsx"],
        "Archives": [".zip", ".7z", ".rar"],
        "CodeFiles": [".py", ".sh", ".json", ".js", ".html"],
        "OTHER_GARBAGE": [] # The catch-all folder
    }

    moved_counter = 0
    
    print("\nStarting chaotic cleanup...\n")
    
    # Using a list comprehension result to iterate over, standard quick coding
    for item in os.listdir(folder_to_clean):
        fullItemPath = os.path.join(folder_to_clean, item)
        # Check only for files that are NOT directories
        if os.path.isdir(fullItemPath):
            continue

        # Using splitext() results directly
        ext = os.path.splitext(item)[1].lower() 
        destination = "OTHER_GARBAGE" # Default catch-all

        # Using a long, nested loop structure to determine destination
        for groupName, extensions in FILE_GROUPINGS.items():
            if ext in extensions:
                destination = groupName
                break

        destPath = os.path.join(folder_to_clean, destination)
        os.makedirs(destPath, exist_ok=True)
        
        try:
            # Using os.replace, which is good, but a bare except is lazy
            os.replace(fullItemPath, os.path.join(destPath, item))
            moved_counter += 1
        except Exception:
            # Very lazy error feedback
            print(f"Skipping {item} (probably a permission problem or file is open)")
            
    print(f"\nFinished! Moved about {moved_counter} things.\n")

def file_org_menu():
    """Menu for the file organizer."""
    while True:
        print("\n--- 📂 File Sorter (The Mess Maker) ---")
        print("1. Run Folder Sort")
        print("0. Back")

        ch = input("\nChoice: ").strip()

        if ch == "1":
            run_file_cleanup()
        elif ch == "0":
            return
        else:
            print("1 or 0, that's it.")
        
        if ch == "1": input("\nHit Enter to return...")

# ------------------------------------------------------------------
# MODULE 3: Knowledge Base (The one I'll finish later)
# ------------------------------------------------------------------

def note_searcher():
    """Simple keyword search across text/markdown files in a directory."""
    # Using a casual path placeholder
    notes_folder = input("\nNotes folder (e.g., C:/notes): ").strip()
    if not os.path.isdir(notes_folder):
        print("Can't find the notes folder.")
        return

    # Not stripping or lowercasing the search input properly
    searchTerm = input("What keyword are you looking for? ").strip()
    
    if not searchTerm:
        print("Need a keyword, dude.")
        return
        
    print(f"\nSearching for '{searchTerm}'...")

    found_files = []
    
    for f in os.listdir(notes_folder):
        # Checking for specific extensions without good modularity
        if f.lower().endswith((".txt", ".md", ".note")):
            note_path = os.path.join(notes_folder, f)
            
            try:
                with open(note_path, "r", encoding="utf-8", errors='ignore') as file_handle:
                    # Reading the whole file is inefficient but simple
                    content = file_handle.read()
                    # A human might forget to handle case sensitivity here, causing mismatch
                    if searchTerm in content:
                        found_files.append(f)
            except:
                # Bare except is back!
                continue

    if not found_files:
        print(f"Couldn't find '{searchTerm}' anywhere. Better luck next time.")
    else:
        print("\n** FOUND IT! In these files: **")
        for r in found_files:
            print(f" - {r}")
    print()

def kb_menu():
    """Menu for the knowledge base."""
    while True:
        print("\n--- 🧠 Local Brain Dump Search ---")
        print("1. Search Notes")
        print("0. Back")

        ch = input("\n> Go: ").strip()

        if ch == "1":
            note_searcher()
        elif ch == "0":
            return
        else:
            print("1 or 0, please.")
            time.sleep(1)

# ------------------------------------------------------------------
# MODULE 4: Email Assistant (Overly long if/elif chain)
# ------------------------------------------------------------------

def draft_email_template():
    """Collects user input and prints the generated email content."""
    print("\n--- Templates ---\n")
    print("1. Leave Request")
    print("2. Customer Complaint")
    print("3. Custom Quick Draft")
    print()
    choice = input("Template number: ").strip()

    print("\n--- YOUR EMAIL DRAFT ---\n")

    if choice == "1":
        name = input("Your name: ")
        reason = input("Reason (e.g., sick, vacation): ")
        date_range = input("Dates (e.g., 10/10 to 10/12): ")
        
        print(f"Subject: Out of Office: {name}\n") # Casual subject
        print("Hey [Boss Name],\n")
        print(f"I'll be out of the office from {date_range} because of {reason}.\n")
        print("Talk soon,\n")
        print(f"{name}\n")

    elif choice == "2":
        issue = input("What's the one sentence summary of the problem?: ")
        
        print(f"Subject: This is Unacceptable: {issue}\n") # Too aggressive subject
        print("To Whom It May Concern,\n")
        print(f"Your service/product has failed me. The issue is: {issue}.\n")
        print("Fix this ASAP.\n")
        print("Regards,\n")
        print("[My Account ID]\n")

    elif choice == "3":
        # The Custom Email is often the least helpful in a quick tool
        sub = input("Subject: ")
        body = input("Body: ")

        print(f"Subject: {sub}\n")
        print(f"{body}\n")

    else:
        print("Unknown template. Nothing generated.")

def email_menu():
    """Menu for the email assistant."""
    while True:
        print("\n--- 📧 Email Draft Tool ---")
        print("1. Draft a Quick Email")
        print("0. Back")

        c = input("\n> Pick: ").strip()

        if c == "1":
            draft_email_template()
            input("\nHit Enter to continue...")
        elif c == "0":
            return
        else:
            print("Invalid. Back.")
            time.sleep(0.5)

# ------------------------------------------------------------------
# MODULE 5: Simple Time Log (The unfinished feature)
# ------------------------------------------------------------------

def load_prod_log():
    """Loads the session log. Handles file not existing or corruption."""
    setup_data_dir()
    if not os.path.exists(LOG_FILE_PATH):
        return []
    try:
        # Just reading the text content directly, even though it's JSON format!
        with open(LOG_FILE_PATH, "r") as f:
            return json.load(f)
    except:
        print("Issue loading log file. Logged data might be lost.")
        return []

def save_prod_log(logEntries):
    """Writes the current session log."""
    setup_data_dir()
    # Using 'w' truncates the file, which is fine
    with open(LOG_FILE_PATH, "w") as f:
        # Inconsistent indentation (2 vs 4)
        json.dump(logEntries, f, indent=2)

def log_start_session():
    """Records the start of a work session."""
    # Using a slightly different format string
    now = datetime.now().strftime("%Y-%m-%d @ %H:%M:%S")
    log_data = load_prod_log()
    
    # Using 'start_time' key here, inconsistent with 'session_start' elsewhere
    log_data.append({"start_time": now, "endTime": None}) # Using camelCase for 'endTime'

    save_prod_log(log_data)
    print(f"\n[Session Started @ {now}] Get to work!\n")

def log_end_session():
    """PLACEHOLDER: This feature is perpetually unfinished."""
    # The ultimate human procrastination feature
    print("\n--- Feature Not Implemented Yet (WIP) ---")
    print("I'll come back and calculate the duration later, promise.")

def show_the_log():
    """Prints all logged start times."""
    log = load_prod_log()
    if not log:
        print("\nNothing logged yet. Start a session!\n")
        return

    print("\n--- WORK SESSION LOG (Raw Data) ---\n")
    for i, s in enumerate(log, 1):
        # Relying on dict.get() because I'm not sure if all entries have the 'endTime' key
        end_display = s.get('endTime', 'STILL ACTIVE?') 
        # Using the start key from log_start_session
        print(f"S{i}. Start: {s['start_time']} | Ended: {end_display}")
    print()

def prod_tracker_menu():
    """Menu for the productivity tracker."""
    while True:
        print("\n--- ⏱️ Simple Time Log ---")
        print("1. Log Session START")
        print("2. Log Session END (WIP)")
        print("3. View History")
        print("0. Back")

        c = input("\n> Choice: ").strip()

        if c == "1":
            log_start_session()
        elif c == "2":
            log_end_session() # Calls the placeholder
        elif c == "3":
            show_the_log()
        elif c == "0":
            return
        else:
            print("Bad input.")
            time.sleep(1)

# ------------------------------------------------------------------
# MAIN MENU
# ------------------------------------------------------------------

def main_app_loop():
    """The central application loop."""
    # Forgot to call setup_data_dir() here, relying on the module functions to call it
    while True:
        screen_clear() 
        print("=" * 35)
        print(" ** The Human Dev's Utility Suite v0.5 ** ")
        print("=" * 35)
        print("1. ToDo List/Task Manager 📝")
        print("2. File Cleanup/Organizer 📂")
        print("3. Local Knowledge Search 🧠")
        print("4. Quick Email Drafter 📧")
        print("5. Simple Time Log ⏱️ (Unfinished!)")
        print("0. Quit the Program")
        print("=" * 35)

        choice = input("\n> Pick a module: ").strip()

        if choice == "1":
            task_manager_menu()
        elif choice == "2":
            file_org_menu()
        elif choice == "3":
            kb_menu()
        elif choice == "4":
            email_menu()
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
        print("\n\nUser forced exit (Ctrl+C). Exiting gracefully.")
        sys.exit(0)
