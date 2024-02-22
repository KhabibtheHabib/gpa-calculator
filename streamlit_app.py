import streamlit as st
import streamlit as st
import pandas as pd
from pathlib import Path

# Function to create an account and save data to CSV
def create_account(username, password, name, email):
    data = pd.DataFrame({"Username": [username], "Password": [password], "Name": [name], "Email": [email]})
    data.to_csv("user_data.csv", index=False)

# Function to sign in and retrieve user data
def sign_in(username, password):
    data = pd.read_csv("user_data.csv")
    user_data = data[(data['Username'] == username) & (data['Password'] == password)]
    return user_data

# Streamlit app
def main():
    st.title("User Account Management")

    # Page state
    page = st.sidebar.radio("Navigation", ["Home", "Create Account", "Sign In"])

    if page == "Home":
        st.subheader("Home Page")
        st.write("Welcome to the User Account Management App!")

    elif page == "Create Account":
        st.subheader("Create Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        name = st.text_input("Full Name")
        email = st.text_input("Email")

        if st.button("Create Account"):
            create_account(username, password, name, email)
            st.success("Account created successfully!")

    elif page == "Sign In":
        st.subheader("Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign In"):
            user_data = sign_in(username, password)
            if not user_data.empty:
                st.success(f"Sign in successful! Welcome, {user_data['Name'].values[0]}")
                st.write("User Information:")
                st.write(user_data)
            else:
                st.error("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()

# Function to calculate GPA
def calculate_gpa(grades):
    grade_points = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
    total_points = sum(grade_points.get(grade, 0) for grade in grades)
    return round(((total_points / len(grades)) * 100)/100)

# Streamlit app
def main():
    st.title("GPA Calculator")

    # Input fields
    grades = []
    for i in range(1, 7):
        st.subheader(f"Class {i}")
        grade = st.selectbox(f"Grade for Class {i}", ['A', 'B', 'C', 'D', 'F'])
        grades.append(grade)

    # Calculate GPA
    if st.button("Calculate GPA"):
        gpa = calculate_gpa(grades)
        st.success(f"Calculated GPA: {gpa}")

if __name__ == "__main__":
    main()
