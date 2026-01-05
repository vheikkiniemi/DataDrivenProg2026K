
import streamlit as st
import sqlite3

conn = sqlite3.connect("crm.db")
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS customer
(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT)""")
conn.commit()

st.title("Asiakasrekisteri")

with st.form("add"):
    name = st.text_input("Nimi")
    email = st.text_input("Sähköposti")
    submitted = st.form_submit_button("Lisää")
    if submitted and name:
        cur.execute("INSERT INTO customer (name,email) VALUES (?,?)",(name,email))
        conn.commit()
        st.success(f"Lisätty: {name}")

st.subheader("Asiakkaat")
rows = cur.execute("SELECT id, name, email FROM customer").fetchall()
st.table(rows)