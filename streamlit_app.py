import streamlit as st
import pandas as pd
from pathlib import Path

# Function to create an account and save data to CSV
def create_account(username, password, name, email, wanted_gpa):
    data = pd.DataFrame({"Username": [username], "Password": [password], "Name": [name], "Email": [email], "WantedGPA": [wanted_gpa]})
    data.to_csv("user_data.csv", index=False)

# Function to sign in and retrieve user data
def sign_in(username, password):
    data = pd.read_csv("user_data.csv")
    user_data = data[(data['Username'] == username) & (data['Password'] == password)]
    return user_data

# Function to input grades for a signed-in user
def input_grades(username, grades):
    data = pd.read_csv("user_data.csv")
    user_index = data[data['Username'] == username].index
    for i, grade in enumerate(grades):
        data.at[user_index, f"Grade{i + 1}"] = grade
    data.to_csv("user_data.csv", index=False)

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
        wanted_gpa = st.number_input("Wanted GPA", min_value=0.0, max_value=4.0, step=0.1)

        if st.button("Create Account"):
            create_account(username, password, name, email, wanted_gpa)
            st.success("Account created successfully!")

    elif page == "Sign In":
        st.subheader("Sign In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Sign In"):
            user_data = sign_in(username, password)
            if not user_data.empty:
                st.success(f"Sign in successful! Welcome, {user_data['Name'].values[0]}")

                # Show user information
                st.write("User Information:")
                st.write(user_data)

                # Allow inputting grades
                grades = []
                for i in range(1, 7):
                    grade = st.number_input(f"Grade {i}", min_value=0, max_value=4, step=0.1, key=f"grade{i}")
                    grades.append(grade)

                if st.button("Input Grades"):
                    input_grades(username, grades)
                    st.success("Grades inputted successfully!")

                # Display actual GPA and wanted GPA
                st.write("GPA Information:")
                st.write(f"Actual GPA: {user_data['WantedGPA'].values[0]}")
                st.write(f"Wanted GPA: {user_data['WantedGPA'].values[0]}")

            else:
                st.error("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()
