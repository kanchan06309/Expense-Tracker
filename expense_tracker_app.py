import streamlit as st
import mysql.connector
from datetime import date
import pandas as pd
import matplotlib.pyplot as plt

# --- Connect to MySQL database ---
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="kanmysql",
        database="expense_tracker"
    )

# --- Add a new expense ---
def add_expense(category, amount, note):
    conn = connect_db()
    cursor = conn.cursor()
    query = "INSERT INTO expenses (date, category, amount, note) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (date.today(), category, amount, note))
    conn.commit()
    conn.close()
    st.success("✅ Expense added successfully!")

# --- Get all expenses as DataFrame ---
def view_expenses():
    conn = connect_db()
    df = pd.read_sql("SELECT * FROM expenses ORDER BY date DESC", conn)
    conn.close()
    return df

# --- Summarize expenses by category ---
def summary_by_category(df):
    return df.groupby("category")["amount"].sum().reset_index()

# --- Streamlit UI ---
st.set_page_config(page_title="Expense Tracker", layout="centered")
st.title("💸 Expense Tracker App")

menu = ["Add Expense", "View Expenses", "Summary by Category", "Spending Chart"]
choice = st.sidebar.radio("Menu", menu)

# --- Add Expense ---
if choice == "Add Expense":
    st.subheader("➕ Add New Expense")
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0.0)
    note = st.text_area("Note")
    if st.button("Add Expense"):
        add_expense(category, amount, note)

# --- View Expenses ---
elif choice == "View Expenses":
    st.subheader("📋 All Expenses")
    df = view_expenses()
    st.dataframe(df)

# --- Summary by Category ---
elif choice == "Summary by Category":
    st.subheader("📊 Summary by Category")
    df = view_expenses()
    summary = summary_by_category(df)
    st.dataframe(summary)

# --- Spending Chart ---
elif choice == "Spending Chart":
    st.subheader("📈 Spending Chart by Category")
    df = view_expenses()
    summary = summary_by_category(df)
    fig, ax = plt.subplots()
    ax.pie(summary["amount"], labels=summary["category"], autopct='%1.1f%%', startangle=90)
    ax.axis("equal")
    st.pyplot(fig)