import streamlit as st
import pandas as pd

# Set the cookies and cream color theme
st.set_page_config(layout="centered", page_icon=":cookie:", page_title="GPA Calculator")
st.markdown("""
<style>
.stApp {
    background-color: #D5C3B0;
    color: #4D2F1D;
}
</style>
""", unsafe_allow_html=True)

# Create a session state to store the login status
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# Login function
def login(username, password):
    # Here, you would implement your authentication logic
    # For this example, we'll use a hardcoded username and password
    if username == "admin" and password == "password":
        st.session_state.is_logged_in = True
        st.success("Login successful!")
    else:
        st.error("Invalid username or password.")

# Logout function
def logout():
    st.session_state.is_logged_in = False
    st.success("Logged out successfully.")

# GPA calculation function
def calculate_gpa(grades):
    # Mapping grade letters to numerical values
    grade_map = {"A+": 4.0, "A": 4.0, "A-": 3.7, "B+": 3.3, "B": 3.0, "B-": 2.7,
                 "C+": 2.3, "C": 2.0, "C-": 1.7, "D+": 1.3, "D": 1.0, "D-": 0.7, "F": 0.0}

    total_credits = 0
    total_points = 0

    for course, grade in grades.items():
        # Assuming credit hours for all courses are 3
        credits = 3
        total_credits += credits

        if grade in grade_map:
            grade_points = grade_map[grade] * credits
            total_points += grade_points

    gpa = total_points / total_credits
    return gpa

# App layout
st.title("GPA Calculator")

if st.session_state.is_logged_in:
    st.sidebar.success("Logged in as admin")
    st.sidebar.button("Logout", on_click=logout)

    # Get user input for grades
    grades = st.text_area("Enter your grades (course: grade)", height=200)

    if grades:
        # Parse the input grades
        grade_dict = {}
        for line in grades.split("\n"):
            if ":" in line:
                course, grade = line.split(":")
                grade_dict[course.strip()] = grade.strip()

        # Calculate GPA
        gpa = calculate_gpa(grade_dict)
        st.success(f"Your GPA is: {gpa:.2f}")

else:
    st.sidebar.info("Please log in to access the GPA calculator.")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    st.sidebar.button("Login", on_click=login, args=(username, password))
