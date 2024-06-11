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


    def add_document(self,collection,data):
         
        try:
            doc_ref = self.db.collection(collection).add(data)
            
            logger.info(f"Document {doc_ref} set with data: {data}")
        except Exception as e:
            logger.error(f"Error adding document {doc_ref}: {e}")



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
        
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc_ref.update(data)
            logger.info(f"Document {doc_id} updated with data: {data}")
        except Exception as e:
            logger.error(f"Error updating document {doc_id}: {e}")

    def delete_document(self, doc_id):
       
        try:
            doc_ref = self.db.collection(self.collection_name).document(doc_id)
            doc_ref.delete()
            logger.info(f"Document {doc_id} deleted.")
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {e}")

    async def upload_photo_to_firebase(self, file_path):
        
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



    def save_telg_message_to_firestore(self, message):
        #save teleg mesgs if not exist 
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

            # self.db.collection(self.collection_name).document(doc_id).set(data)
            self.create_document_if_not_exists(doc_id=doc_id,data=data)  
            logger.info(f"Message {doc_id} saved to Firestore.")
        except Exception as e:
            logger.error(f"Error saving message {message} to Firestore: {e}")

    
    
    
    def get_documents_where_ai_is_false(self,collection_name="telegramMessages"):
        """
        Get all documents where the 'ai' field is False.

        :return: A list of documents where 'ai' is False.
        """

        try:
            query = self.db.collection(collection_name).where('ai', '==', False)
            logger.info(f"query {query}")
            docs = query.stream()
            results = []
            for doc in docs:
                doc_dict = doc.to_dict()
                doc_dict['id'] = doc.id  # Add the document ID to the dictionary
                results.append(doc_dict)
           
            logger.info(f"Retrieved {len(results)} documents--> {collection_name}--> where 'ai' is False.")
            if len(results) == 0:
               logger.warn(f"Retrieved  0 mesages ")

            return results
        except Exception as e:
            logger.error(f"Error querying documents where 'ai' is False: {e}")
            return []
        



    def get_documents_where_sent_is_false(self,collection_name="teleg" ):
        
        try:
            query = self.db.collection(collection_name).where('sent', '==', False)
            docs = query.stream()
            results = []
            for doc in docs:
                doc_dict = doc.to_dict()
                doc_dict['id'] = doc.id  # Add the document ID to the dictionary
                results.append(doc_dict)
                doc_ref = self.db.collection(collection_name).document(doc.id)
                doc_ref.update({
                    'sent':True
                })
           
            logger.info(f"Retrieved {len(results)} documents where 'ai' is False.")
            return results
        except Exception as e:
            logger.error(f"Error querying documents where 'ai' is False: {e}")
            return []





    def create_document_if_not_exists(self,doc_id, data):
        doc_ref = self.db.collection(self.collection_name).document(doc_id)
        try:
            transaction = self.db.transaction()
            @firestore.transactional
            def transactional_create(transaction, doc_ref):
                snapshot = doc_ref.get(transaction=transaction)
                if not snapshot.exists:
                    transaction.set(doc_ref, data)
                else:
                    logger.info('Document already exists')
            transactional_create(transaction, doc_ref)
            logger.info('Document successfully created!')
        except Exception as e:
            logger.warning(f'Transaction failed: {e}')

    # schudel
    def create_schudel_time(self, data):
        try:
            doc_ref = self.db.collection("schudel").add(data)
            logger.info('Schudel document successfully created!')
        except Exception as e:
            logger.warning(f'Transaction failed: {e}')

    def get_scheduled_msgs_not_sent(self):
        try:
            query = self.db.collection("schudel").where('sent', '==', False)
            docs = query.stream()
            results = []
            for doc in docs:
                doc_dict = doc.to_dict()
                doc_dict['id'] = doc.id  # Add the document ID to the dictionary
                results.append(doc_dict)

            logger.info(f"Retrieved {len(results)} documents where 'sent' is False.")
            if len(results) == 0:
                logger.warning("Retrieved 0 messages")

            return results
        except Exception as e:
            logger.error(f"Error querying documents where 'sent' is False: {e}")
            return []

    def set_scheduled_msg_as_sent(self, doc_id):
        try:
            doc_ref = self.db.collection("schudel").document(doc_id)
            doc = doc_ref.get()
            if not doc.exists:
                logger.warning(f"No document found with ID: {doc_id}")
            else:
                doc_ref.update({
                    'sent': True
                })
                logger.info(f"Document with ID {doc_id} marked as sent.")
        except Exception as e:
            logger.error(f"Error updating document with ID {doc_id}")

# token Metrics
            
   


   





    def get_token_metrics_documents_where_sent_is_false_telg(self):
        
        """
        Get all documents where the 'sent' field is False.

        :return: A list of documents where  'sent' is False.
        """
        try:
            query = self.db.collection("teleg").where('sent', '==', False)
            docs = query.stream()
            results = []
            for doc in docs:
                doc_dict = doc.to_dict()
                doc_dict['id'] = doc.id  # Add the document ID to the dictionary
                results.append(doc_dict)
                doc_ref = self.db.collection("teleg").document(doc.id)
                doc_ref.update({
                    'sent':True
                })
           
            logger.info(f"Retrieved {len(results)} documents where 'ai' is False.")
            return results
        except Exception as e:
            logger.error(f"Error querying documents where 'ai' is False: {e}")
            return []    


