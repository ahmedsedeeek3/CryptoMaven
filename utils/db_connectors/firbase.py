import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, storage
from utils.logging.logginconfig import setup_logger
from datetime import datetime

logger = setup_logger(__name__)

class FirebaseClient:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(FirebaseClient, cls).__new__(cls)
        return cls._instance

    def __init__(self, app_name, collection_name):
        if not hasattr(self, 'initialized') or not self.initialized:
            self._initialize_firebase(app_name, collection_name)
            self.initialized = True

    def _initialize_firebase(self, app_name, collection_name):
        self.credentials_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
        if not self.credentials_json:
            raise FileNotFoundError("Environment variable FIREBASE_CREDENTIALS_JSON not set.")

        credentials_dict = json.loads(self.credentials_json)
        self.cred = credentials.Certificate(credentials_dict)
        
        # Initialize Firebase app if not already initialized
        if not firebase_admin._apps:
            self.app = firebase_admin.initialize_app(self.cred, {
                'storageBucket': 'gs://mytestagent-1ab6f.appspot.com'
            }, name=app_name)
        else:
            self.app = firebase_admin.get_app(app_name)
            
        self.db = firestore.client(app=self.app)
        self.bucket = storage.bucket(name='mytestagent-1ab6f.appspot.com', app=self.app)
        self.collection_name = collection_name
        
    def set_document(self, doc_id, data):
        """
        Set the data for a specified document in the Firestore collection.

        :param doc_id: Document ID.
        :param data: Dictionary containing the data to be set in the document.
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc_ref.set(data)
            logger.info(f"Document {doc_id} set with data: {data}")
        except Exception as e:
            logger.error(f"Error setting document {doc_id}: {e}")

    def get_document(self, doc_id):
        """
        Retrieve the data for a specified document in the Firestore collection.

        :param doc_id: Document ID.
        :return: Dictionary containing the data of the document.
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc = doc_ref.get()
            if doc.exists:
                logger.info(f"Document {doc_id} data: {doc.to_dict()}")
                return doc.to_dict()
            else:
                logger.info(f"Document {doc_id} does not exist.")
                return None
        except Exception as e:
            logger.error(f"Error getting document {doc_id}: {e}")
            return None

    def update_document(self, doc_id, data):
        """
        Update the data for a specified document in the Firestore collection.

        :param doc_id: Document ID.
        :param data: Dictionary containing the data to be updated in the document.
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc_ref.update(data)
            logger.info(f"Document {doc_id} updated with data: {data}")
        except Exception as e:
            logger.error(f"Error updating document {doc_id}: {e}")

    def delete_document(self, doc_id):
        """
        Delete a specified document from the Firestore collection.

        :param doc_id: Document ID.
        """
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc_ref.delete()
            logger.info(f"Document {doc_id} deleted.")
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")

    async def upload_photo_to_firebase(self, file_path):
        """
        Upload a photo to Firebase Storage.

        :param file_path: Path to the photo file.
        :return: URL of the uploaded photo.
        """
        try:
            blob = self.bucket.blob(os.path.basename(file_path))
            blob.upload_from_filename(file_path)
            blob.make_public()
            url = blob.public_url
            logger.info(f"Uploaded photo to {url}")
            return url
        except Exception as e:
            logger.error(f"Error uploading photo {file_path}: {e}")
            return None

    def save_message_to_firestore(self, message):
        """
        Save a message to Firestore, including an optional photo URL.

        :param message: Telegram message object.
        :param photo_path: Path to the uploaded photo.
        :param img: Image data to be saved.
        """
        try:
            doc_id = str(message['id'])
            data = {
                "ai": False,  
                'date': message['date'].isoformat(),
                'message': message['message'],
                'pinned': message['pinned'],
                'views': message.get('views', 0),
                'ttl_period': message.get('ttl_period', None),
                
            }

            self.db.collection(self.collection_name).document(doc_id).set(data)
            logger.info(f"Message {doc_id} saved to Firestore.")
        except Exception as e:
            logger.error(f"Error saving message {message} to Firestore: {e}")

    
    
    
    def get_documents_where_ai_is_false(self):
        """
        Get all documents where the 'ai' field is False.

        :return: A list of documents where 'ai' is False.
        """
        try:
            query = self.db.collection(self.collection_name).where('ai', '==', False)
            docs = query.stream()
            results = []
            for doc in docs:
                doc_dict = doc.to_dict()
                doc_dict['id'] = doc.id  # Add the document ID to the dictionary
                results.append(doc_dict)
           
            logger.info(f"Retrieved {len(results)} documents where 'ai' is False.")
            return results
        except Exception as e:
            logger.error(f"Error querying documents where 'ai' is False: {e}")
            return []
        



    def get_documents_where_sent_is_false_telg(self):
        
        """
        Get all documents where the 'sent' field is False.

        :return: A list of documents where 'ai' is False.
        """
        try:
            query = self.db.collection("teleg").where('sent', '==', False)
            docs = query.stream()
            results = []
            for doc in docs:
                doc_dict = doc.to_dict()
                doc_dict['id'] = doc.id  # Add the document ID to the dictionary
                results.append(doc_dict)
           
            logger.info(f"Retrieved {len(results)} documents where 'ai' is False.")
            return results
        except Exception as e:
            logger.error(f"Error querying documents where 'ai' is False: {e}")
            return []

