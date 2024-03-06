import csv
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# Global variables
CLASSES = 6
USER_DATA = 'user_data.csv'
GRADE_MAPPING = {'A+': 4.0, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7, 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.7, 'F': 0.0}

# Functions
def signup():
    username = entry_username.get()
    password = entry_password.get()
    desired_gpa = float(entry_desired_gpa.get())

    # Check if username already exists
    with open(USER_DATA, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username:
                messagebox.showerror("Error", "Username already exists!")
                return

    # Create new user
    with open(USER_DATA, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, password, desired_gpa] + [''] * CLASSES)

    messagebox.showinfo("Success", "Account created successfully!")

def login():
    username = entry_username.get()
    password = entry_password.get()

    # Check if username and password are correct
    with open(USER_DATA, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == username and row[1] == password:
                show_grades_window(row)
                return

    messagebox.showerror("Error", "Invalid username or password!")

def show_grades_window(user_data):
    grades_window = tk.Toplevel(root)
    grades_window.title(f"Grades - {user_data[0]}")

    # Labels for classes
    class_labels = []
    for i in range(CLASSES):
        label = tk.Label(grades_window, text=f"Class {i+1}:")
        label.grid(row=i, column=0)
        class_labels.append(label)

    # Entry boxes for grades
    grade_entries = []
    for i in range(CLASSES):
        entry = tk.Entry(grades_window)
        entry.grid(row=i, column=1)
        entry.insert(0, user_data[i+3])
        grade_entries.append(entry)

    # Save button
    save_button = tk.Button(grades_window, text="Save", command=lambda: save_grades(user_data, grade_entries))
    save_button.grid(row=CLASSES, column=0, columnspan=2)

    # Plot button
    plot_button = tk.Button(grades_window, text="Plot Performance", command=lambda: plot_performance(user_data, grade_entries))
    plot_button.grid(row=CLASSES+1, column=0, columnspan=2)

def save_grades(user_data, grade_entries):
    with open(USER_DATA, 'r') as file:
        reader = csv.reader(file)
        data = list(reader)

    for i, row in enumerate(data):
        if row[0] == user_data[0]:
            for j in range(CLASSES):
                data[i][j+3] = grade_entries[j].get().upper()
            break

    with open(USER_DATA, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    messagebox.showinfo("Success", "Grades saved successfully!")

def plot_performance(user_data, grade_entries):
    grades = [GRADE_MAPPING.get(entry.get().upper(), 0) for entry in grade_entries]
    plt.plot(range(1, CLASSES+1), grades)
    plt.axhline(y=user_data[2], color='r', linestyle='--', label=f'Desired GPA: {user_data[2]}')
    plt.xlabel('Class')
    plt.ylabel('Grade')
    plt.title(f'Performance - {user_data[0]}')
    plt.legend()
    plt.show()

# GUI
root = tk.Tk()
root.title("Grade Tracker")

# Signup frame
signup_frame = tk.Frame(root)
signup_frame.pack(padx=20, pady=20)

label_username = tk.Label(signup_frame, text="Username:")
label_username.grid(row=0, column=0)

entry_username = tk.Entry(signup_frame)
entry_username.grid(row=0, column=1)

label_password = tk.Label(signup_frame, text="Password:")
label_password.grid(row=1, column=0)

entry_password = tk.Entry(signup_frame, show="*")
entry_password.grid(row=1, column=1)

label_desired_gpa = tk.Label(signup_frame, text="Desired GPA:")
label_desired_gpa.grid(row=2, column=0)

entry_desired_gpa = tk.Entry(signup_frame)
entry_desired_gpa.grid(row=2, column=1)

signup_button = tk.Button(signup_frame, text="Sign Up", command=signup)
signup_button.grid(row=3, column=0, columnspan=2, pady=10)

login_button = tk.Button(signup_frame, text="Login", command=login)
login_button.grid(row=4, column=0, columnspan=2)

root.mainloop()
