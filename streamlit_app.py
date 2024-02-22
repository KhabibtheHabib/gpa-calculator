import streamlit as st

# Function to calculate GPA
def calculate_gpa(grades):
    grade_points = {'A': 4, 'B': 3, 'C': 2, 'D': 1, 'F': 0}
    total_points = sum(grade_points.get(grade, 0) for grade in grades)
    return round((total_points / len(grades)) * 100)

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
