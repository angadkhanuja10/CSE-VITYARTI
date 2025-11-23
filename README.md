# Productivity & Automation

## Overview of the Project

This project is a multi-module Python application designed to streamline
daily productivity by combining several useful tools into one system. It
includes modules for task management, file organization, note searching,
email drafting, and productivity logging. The program runs entirely in
the console and focuses on simplicity, modular design, and user-friendly
interaction. Each feature works independently but is connected through a
main controller, making it easy to navigate and use without requiring
any external dependencies or databases.

## Features

-   **Task Manager:** Add, update, delete, and mark tasks as completed.
-   **File Organizer:** Automatically organize files based on extensions
    (images, PDFs, videos, docs).
-   **Note Search Tool:** Search for keywords inside `.txt` files across
    folders.
-   **Email Draft Generator:** Create simple, ready-to-edit email
    templates.
-   **Productivity Logger:** Record daily work hours and notes using
    JSON storage.
-   **Modular Navigation:** Each feature works as a separate module for
    easy maintenance.
-   **Error Handling:** Prevents crashes due to invalid inputs or
    missing files.

## Technologies / Tools Used

-   **Python 3.x**
-   **OS Library**
-   **Shutil Library**
-   **JSON Library**
-   **Datetime Library**
-   Cross‑platform clear‑screen support

## Steps to Install & Run the Project

1.  Install **Python 3.x**.
2.  Download or clone the project.
3.  Open terminal/command prompt in the project directory.
4.  Run:
    python main.py

5.  Use the menu to navigate between modules.

## Instructions for Testing

-   Test each module individually.
-   Add/update/delete tasks to verify JSON storage.
-   Run file organizer on folders with mixed file types.
-   Search different keywords in multiple `.txt` files.
-   Generate email drafts to confirm formatting.
-   Add multiple productivity logs and verify updates.
-   Test invalid inputs and incorrect paths to ensure error handling
    works.

