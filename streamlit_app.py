import os
import logging
from dotenv import load_dotenv
import streamlit as st
import pandas as pd

# Load environment variables
load_dotenv()
DB_PATH = os.getenv("DB_PATH", "user_data.csv")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_account(username, password, name, email, wanted_gpa):
    """
    Create a new user account and save data to the database.

    Args:
        username (str): The username for the new account.
        password (str): The password for the new account.
        name (str): The full name of the user.
        email (str): The email address of the user.
        wanted_gpa (float): The desired GPA for the user.

    Returns:
        None
    """
    data = pd.DataFrame({"Username": [username], "Password": [password], "Name": [name], "Email": [email], "WantedGPA": [wanted_gpa]})
    data.to_csv(DB_PATH, mode='a', header=False, index=False)
    logging.info(f"New account created for {name} ({username})")

def sign_in(username, password):
    """
    Sign in a user and retrieve their data from the database.

    Args:
        username (str): The username for the account.
        password (str): The password for the account.

    Returns:
        pandas.DataFrame: The user data if the sign-in is successful, otherwise an empty DataFrame.
    """
    data = pd.read_csv(DB_PATH)
    user_data = data[(data['Username'] == username) & (data['Password'] == password)]
    if not user_data.empty:
        logging.info(f"Sign-in successful for {username}")
        return user_data
    else:
        logging.warning(f"Sign-in failed for {username}")
        return pd.DataFrame()

def input_grades(username, grades):
    """
    Input grades for a signed-in user and update the database.

    Args:
        username (str): The username for the account.
        grades (list): A list of up to 6 grades.

    Returns:
        None
    """
    data = pd.read_csv(DB_PATH)
    user_index = data[data['Username'] == username].index
    for i, grade in enumerate(grades):
        data.at[user_index, f"Grade{i + 1}"] = grade
    data.to_csv(DB_PATH, index=False)
    logging.info(f"Grades updated for {username}")

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
                    grade = st.number_input(f"Grade {i}", min_value=0.0, max_value=4.0, step=0.1, key=f"grade{i}")
                    grades.append(grade)

                if st.button("Input Grades"):
                    input_grades(username, grades)
                    st.success("Grades inputted successfully!")

                # Display actual GPA and wanted GPA
                st.write("GPA Information:")
                st.write(f"Actual GPA: {sum(grades) / len(grades):.2f}")
                st.write(f"Wanted GPA: {user_data['WantedGPA'].values[0]}")

            else:
                st.error("Invalid username or password. Please try again.")

if __name__ == "__main__":
    main()
