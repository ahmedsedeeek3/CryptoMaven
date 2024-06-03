import streamlit as st
import bcrypt
import yaml
from yaml.loader import SafeLoader

# Define a function to check passwords
def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

# Load the users from the yaml file
with open('config.yaml') as file:
    users = yaml.load(file, Loader=SafeLoader)

# Authentication function
def authenticate(username, password):
    if username in users and check_password(password, users[username]["password"]):
        return True
    return False

# Streamlit app
st.title("Login")

# Session state to keep track of login status
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if st.session_state.authenticated:
    st.success(f"Welcome {users[st.session_state.username]['name']}!")

    st.title("Streamlit App")

    st.header("Create a new item")
    name = st.text_input("Item name")
    price = st.number_input("Item price", min_value=0.0, step=0.01)
    is_offer = st.checkbox("Is offer?")

    if st.button("Create Item"):
        item_data = {
            "name": name,
            "price": price,
            "is_offer": is_offer
        }
        st.success("Item created successfully!")
        st.json(item_data)

    st.header("Get item details")
    item_id = st.number_input("Item ID", min_value=1, step=1)
    query = st.text_input("Query parameter (optional)")

    if st.button("Get Item"):
        item_data = {
            "item_id": item_id,
            "query": query
        }
        st.success("Item retrieved successfully!")
        st.json(item_data)

    st.header("Update an item")
    update_item_id = st.number_input("Item ID to update", min_value=1, step=1)
    update_name = st.text_input("Updated item name")
    update_price = st.number_input("Updated item price", min_value=0.0, step=0.01)
    update_is_offer = st.checkbox("Is offer?", key="update_is_offer")

    if st.button("Update Item"):
        update_data = {
            "name": update_name,
            "price": update_price,
            "is_offer": update_is_offer
        }
        st.success("Item updated successfully!")
        st.json(update_data)

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.experimental_rerun()
else:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success("Login successful")
            st.experimental_rerun()
        else:
            st.error("Username or password is incorrect")
