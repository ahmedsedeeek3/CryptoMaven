import streamlit as st
import bcrypt
import yaml
from yaml.loader import SafeLoader
import time
class authView:
    def __init__(self) -> None:
        self.users = None
        
    def check_password(self, password, hashed):
        return bcrypt.checkpw(password.encode(), hashed.encode())

    def load_users(self):
        if not self.users:
            with open('config.yaml') as file:
                self.users = yaml.load(file, Loader=SafeLoader)
        
    def authenticate(self, username, password):
        self.load_users()
        if username in self.users and self.check_password(password, self.users[username]["password"]):
            return True
        return False

    def view(self):
        
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
              

        if st.session_state.authenticated:
            self.load_users()
            #st.success(f"Welcome {self.users.get(st.session_state.username, {}).get('name', 'User')}!")
            # add view her
            return  self.users.get(st.session_state.username, {}).get('name', 'User')
        else:
            st.title("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if self.authenticate(username, password):
                    st.session_state.authenticated = True
                    st.session_state.username = username
                    st.success("Login successful")
                    st.rerun()
                else:
                    st.error("Username or password is incorrect")

# Instantiate and call the view method
# auth = authView()
# auth.view()
