import os
import time
from utils.logging.logginconfig import setup_logger
from model.open_ai_prompets import OpenAiPrombet
from dotenv import load_dotenv
from model.collections import collectionNameing




load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

logging = setup_logger(__name__)
collections_names = collectionNameing().collection_name()

class OpenAIGen:
    def __init__(self,openai_clint,firbase_clint) -> None:
        self.openAi = openai_clint
        self.firebase_client = firbase_clint
        self.OpenAiPrombet= OpenAiPrombet()
        '''
        respos:call db for (not AI) not yet reviesed and genrat differen
        messages for differen targets 
        '''
        self.collection_nameing =collections_names

        self.sysROlPrombet = {
            "teleg": '''
                    Read the following text and generate an engaging telegram message listing the trending cryptocurrency coins must with
                    their ticker symbols, and price change. Use relevant emojis to make it attractive. add if possible  links or social media references.
                    End with a call to action to follow for hourly insights don't miss any coin @cryptoMissionX.
                    use only price data form the user prombet data .if you miss price never show it never get price for your brain.
                    Tweet Example:
                    🔥 short lovely intro:
                    all coins don't miss any one in list
                    Follow us for hourly insights!
                    formatting should be list ,should use /\n to end line
                    '''
        }

    def get_generate_teleg_savedb(self):
        self.openAi.set_system_message(self.OpenAiPrombet.teleg_generator_prombt())
        docs = self.firebase_client.get_documents_where_ai_is_false()   
        if len(docs)== 0 :
            logging.warning(msg="ERRO doc retrived with ai false len is 0")
            
            return 
        
        msgs = ""
     
        for doc in docs:
            try:
                doc_id = doc["id"]   
                
                if not doc_id:
                    logging.error("Document does not contain an 'id' field")
                    continue

                message = doc.get('message', False)
                if not message:
                    continue
                
                logging.info(msg=f"mesg from db{message}")  
                ref = self.firebase_client.db.collection("telegramMessages").document(doc_id)
                ref.update({"ai": True})
                msgs += message + "\n" 
                
            except Exception as e:
                logging.error(f"Error processing document {doc.get('id', 'unknown')}: {e}")
        
            
        if not msgs:
            logging.warning("No valid messages found to process")
            return


        logging.info(f"Total messages: {msgs}")
        response = self.openAi.get_response(msgs)

        # Split message if it exceeds Telegram's character limit
        

        doc = {
            "ai_message": response[0],
            "used_token":response[1],
            "source": msgs,
            "sent": False,
            "tar_platform":"telegam",
            "src_grad":1
        }

        try:

            self.firebase_client.db.collection(self.collection_nameing.get("teleg", "")).add(doc)
            logging.info(f"doc add to db {doc}")
            
        except Exception as e:
           
            logging.info(f"error adding document to db {e}")

        
    def generate_coin_metric_sentims_savedb_step1(self):
        
    # Retrieve documents where 'ai' is False
        docs = self.firebase_client.get_documents_where_ai_is_false(collection_name="sementem")

        # Check if there are no documents retrieved
        if not docs:
            logging.warning("ERROR: No documents retrieved where 'ai' is False")
            return

        # Initialize a list to collect messages
        answers = []

        # Process each document
        for doc in docs:
            try:
                doc_id = doc.get("id")
                if not doc_id:
                    logging.error("Document does not contain an 'id' field")
                    continue

                answer_list = doc.get('answer')
                if not answer_list:
                    continue

                logging.info(f"Message from DB: {answer_list}")

                # Update the document in Firestore
                ref = self.firebase_client.db.collection("sementem").document(doc_id)
                ref.update({"ai": True})

                # Collect the messages
                answers.extend(answer_list)

            except Exception as e:
                logging.error(f"Error processing document {doc.get('id', 'unknown')}: {e}")

        # Initialize lists for combined messages
        combined_news = []
        combined_redit = []
        combined_twitter = []

        # Process each answer
        for single_answer in answers:
            MARKET_SENTIMENT_GRADE = single_answer.get("MARKET_SENTIMENT_GRADE")
            MARKET_SENTIMENT_LABEL = single_answer.get("MARKET_SENTIMENT_LABEL")
            NEWS_SENTIMENT_GRADE = single_answer.get("NEWS_SENTIMENT_GRADE")
            NEWS_SENTIMENT_LABLE = single_answer.get("NEWS_SENTIMENT_LABEL")
            NEWS_SUMMARY = single_answer.get("NEWS_SUMMARY")
            REDDIT_SENTIMENT_GRADE = single_answer.get("REDDIT_SENTIMENT_GRADE")
            REDDIT_SENTIMENT_LABEL = single_answer.get("REDDIT_SENTIMENT_LABEL")
            REDDIT_SUMMARY = single_answer.get("REDDIT_SUMMARY")
            TWITTER_SENTIMENT_GRADE = single_answer.get("TWITTER_SENTIMENT_GRADE")
            TWITTER_SENTIMENT_LABEL = single_answer.get("TWITTER_SENTIMENT_LABEL")
            TWITTER_SUMMARY = single_answer.get("TWITTER_SUMMARY")

            # Combine the messages
            combined_news.append(f"market sentiment grade is {MARKET_SENTIMENT_GRADE} and it label is : {MARKET_SENTIMENT_LABEL} news sentiment grade is{NEWS_SENTIMENT_GRADE} its label is :{NEWS_SENTIMENT_LABLE}news summery is : {NEWS_SUMMARY}")
            combined_redit.append(f"market sentiment grade is{MARKET_SENTIMENT_GRADE}and it label is :{MARKET_SENTIMENT_LABEL} sentiment grade is{REDDIT_SENTIMENT_GRADE} {REDDIT_SENTIMENT_LABEL} {REDDIT_SUMMARY}")
            combined_twitter.append(f"market sentiment grade is{MARKET_SENTIMENT_GRADE} and it label is :{MARKET_SENTIMENT_LABEL} {TWITTER_SENTIMENT_GRADE} {TWITTER_SENTIMENT_LABEL} twitter summery  {TWITTER_SUMMARY}")

        # Convert combined messages to strings
        combined_news_str = " ".join(combined_news)
        combined_redit_str = " ".join(combined_redit)
        combined_twitter_str = " ".join(combined_twitter)

        logging.info(f"Total combined messages (news): {combined_news_str}")
        logging.info(f"Total combined messages (redit): {combined_redit_str}")
        logging.info(f"Total combined messages (twitter): {combined_twitter_str}")

        # Get responses from OpenAI
        self.openAi.set_system_message(self.OpenAiPrombet.twitter_sentiment_generator_prombt())
        news_response = self.openAi.get_response(combined_news_str)
        redit_response = self.openAi.get_response(combined_redit_str)
        twitter_response = self.openAi.get_response(combined_twitter_str)

        # Prepare documents for database insertion
        docs_to_add = [
            {
                "ai_message": news_response[0],
                "used_token": news_response[1],
                "source": combined_news_str,
                "ai": False,
                "tar_platform": "twitter",
                "source_platform": "coin_metric",
                "source_label": "sentims_news",
                "src_grad": 1
            },
            {
                "ai_message": redit_response[0],
                "used_token": redit_response[1],
                "source": combined_redit_str,
                "ai": False,
                "tar_platform": "telegam",
                "source_platform": "coin_metric",
                "source_label": "sentims_redit",
                "src_grad": 1
            },
            {
                "ai_message": twitter_response[0],
                "used_token": twitter_response[1],
                "source": combined_twitter_str,
                "ai": False,
                "tar_platform": "telegam",
                "source_platform": "coin_metric",
                "source_label": "sentims_twitter",
                "src_grad": 1
            }
        ]

        # Add documents to Firestore
        try:
            for doc in docs_to_add:
                self.firebase_client.db.collection(self.collection_nameing.get("ready_to_sent_1", "")).add(doc)
            logging.info(f"Documents added to DB: {docs_to_add}")
        except Exception as e:
            logging.error(f"Error adding documents to DB: {e}")


    
    def sentiment_to_db_from_db_step2(self):
            try:
                # 1. Collect documents from the database where 'sent' is False
                docs = self.firebase_client.get_documents_where_ai_is_false(collection_name=collections_names.get("ready_to_sent_1"))
                logging.info(f"Retrieved sentiment from DB: {docs}")
                
                if not docs:
                    logging.warning("ERROR: No documents retrieved where 'sent' is False")
                    return
            except Exception as e:
                logging.error(f"Error querying documents where 'sent' is False: {e}")
                return

            all_messages_list = []
            
            # 2. Iterate over the list of documents
            for doc in docs:
                try:
                    doc_id = doc.get("id")
                    if not doc_id:
                        logging.error("Document does not contain an 'id' field")
                        continue

                    mesg = doc.get('ai_message')
                    if not mesg:
                        logging.error("Error ai_message not found ")
                        continue
                    all_messages_list.append(mesg)
                    logging.info(f"Message from DB: {mesg}")
                    
                    # Update the document in Firestore
                    coll_name = collections_names.get("ready_to_sent_1")
                    ref = self.firebase_client.db.collection(coll_name).document(doc_id)
                    ref.update({"ai2": True})
                except Exception as e:
                    logging.error(f"Error processing document {doc.get('id', 'unknown')}: {e}")
                    continue

            if not all_messages_list:
                logging.warning("No messages to process.")
                return

            all_messages_str = " ".join(all_messages_list)

            try:
                # 3. Call AI to enhance the messages
                prompt = self.OpenAiPrombet.twitter_sentiment_generator_prombt()
                self.openAi.set_system_message(system_message=prompt)
                res = self.openAi.get_response(user_message=all_messages_str)
            except Exception as e:
                logging.error(f"Error processing AI response: {e}")
                return

            # 4. Split the response into multiple messages
            mesg = {
                "ai_message": res[0],
                "used_token": res[1],
                "source": all_messages_str,
                "sent": False,
                "tar_platform": "telegam",
                "source_platform": "coin_metric",
                "source_label": "sentims_twitter",
                "src_grad": 1
            }
            
            try:
                # 5. Store each message in the next collection and prepare for sending
                coll_name = collections_names.get("ready_to_sent_st2")
                self.firebase_client.db.collection(coll_name).add(mesg)
                logging.info("Message added to DB: ")
            except Exception as e:
                logging.error(f"Error storing messages in the database: {e}")
           