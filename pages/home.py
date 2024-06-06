import streamlit as st
from dotenv import load_dotenv
import os
import logging
from utils.logging.logginconfig import setup_logger
from utils.social_conctors.telegramUser import TelegramUserListener

logger = setup_logger(__name__)

load_dotenv()

# losd env
API_ID = int(os.getenv("AP_id"))
API_HASH = os.getenv("App_api_hash")
if not API_ID or not API_HASH:
    logger.log("Issue with keys: API_ID and/or API_HASH are not set properly.")
    exit(1)
#get telegram feeds 




     















def main():
            TeleClient = TelegramUserListener(session_name="reader",
                                  api_id=API_ID,
                                  api_hash=API_HASH,
                                  target_bot_username="@trending")

            TeleClient.run()
            

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
        