import openai
from dotenv import load_dotenv
import os
from pymongo import MongoClient  # Import MongoDB client
from datetime import datetime


# Load environment variables from .env file
load_dotenv()
client = openai.OpenAI()
openai.api_key = os.getenv('OPENAI_API_KEY')



def generate_response(query, user_id):
    # Use the existing assistant's ID
    assistant_id = "asst_5zif5z871bMT2SAOSUV9MmYt"  # Ensure this is the correct assistant ID for classification
    
    # Initialize MongoDB client
    mongo_client = MongoClient(os.getenv('MONGODB_URI'))  # Ensure you have the MongoDB URI in your .env
    db = mongo_client['customer_support']  # Replace with your database name
    conversations_collection = db['conversation']  # Replace with your collection name

    # Create a new communication thread
    thread_python = client.beta.threads.create()

    # Create a message to classify the query in the new thread
    message = client.beta.threads.messages.create(
        thread_id=thread_python.id,  # Use the new thread ID
        role="user",
        content=(
            "You are an MTN customer support chatbot designed to provide factual and helpful information about MTN's products, services, policies, and support. "
            "You must only respond to questions directly related to MTN and within the scope of the data you were trained on. "
            "For any unrelated queries or questions outside your training data, politely inform the user that you can only assist with MTN-specific topics and guide them back to MTN-related support if necessary. "
            "Avoid speculation or providing information outside your designated scope. Always ensure your responses are accurate, clear, and concise. "
            f"Kindly provide a response to the following query: {query}"
        ),
    )

    # Create and wait for the run to complete
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_python.id,
        assistant_id=assistant_id,
    )

    print("Run completed with status: " + run.status)  # Print the run completion status

    # If the run status is "completed", retrieve and print all messages
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_python.id)
        for message in messages:
            if message.role == "assistant":  # Check if the message is from the assistant
                # Extract the content and remove unwanted parts
                response_content = message.content[0].text.value.strip()
                cleaned_response = response_content.split("【")[0].strip()  # Remove everything after "【"
                conversations_collection.insert_one({
                    "user_id": user_id,
                    "query": query,
                    "response": cleaned_response,
                    "timestamp": datetime.utcnow()  # Store the timestamp
    })
                return cleaned_response  # Return the cleaned response

    return "NULL"  # Return NULL if no valid category is found



def generate_category(query):
    # Use the existing assistant's ID
    assistant_id = "asst_5zif5z871bMT2SAOSUV9MmYt"  # Replace with your actual assistant ID

    # Create a new communication thread
    thread_python = client.beta.threads.create()

    # Create a message to classify the query in the new thread
    message = client.beta.threads.messages.create(
        thread_id=thread_python.id,  # Use the new thread ID
        role="user",
        content=(
            "You are an MTN customer support chatbot designed to classify user queries into one of the following distinct categories based on the content of the query: "
            "AYOBA APP DOWNLOAD REQUEST, DATA BUNDLE ACTIVATION REQ, DATA BUNDLE AUTORENEWAL ACTIVATION REQ, DATA BUNDLE BALANCE REQ, "
            "DATA BUNDLE STOP AUTORENEWAL, 2CANPLAY REQUEST, 40 AND FABULOUS GAME REQUEST, 5 LOTTOS REQUEST, APPPLUS GAMES REQUEST, "
            "APPSCLUB REQUEST, BETATALK MIGRATION REQ, BIZCLASS MIGRATION REQ, BIZCONNECT MIGRATION REQ, BIZPLUS MIGRATION REQ, MPULSE MIGRATION REQ. "
            "Your task is to analyze each incoming query and accurately classify it into the most relevant category based on the user's request. "
            "If the query does not clearly fit into one of the categories above, assign NULL as the classification. "
            "Always ensure your classification is precise, distinct, and directly relevant to the content of the query. "
            "Do not assign a query to a category that does not match its intent. If a query is unrelated to the specified categories, return NULL. "
            "Ensure that your classifications are clear, concise, and avoid ambiguity. Only assign queries to the appropriate categories based on the specific nature of MTN's services. "
            f"Classify the following query into a category: {query}"
        ),
    )

    # Create and wait for the run to complete
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_python.id,
        assistant_id=assistant_id,
    )

    print("Run completed with status: " + run.status)  # Print the run completion status

    # If the run status is "completed", retrieve and print all messages
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread_python.id)
        for message in messages:
            if message.role == "assistant":  # Check if the message is from the assistant
                # Extract the content and remove unwanted parts
                response_content = message.content[0].text.value.strip()
                cleaned_response = response_content.split("【")[0].strip()  # Remove everything after "【"
                return cleaned_response  # Return the cleaned response

    return "NULL"  # Return NULL if no valid category is found


def handle_get_response_for_user(query, user_id):
    # Create a completion request to check if the query is in scope
    completion = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=50,
        temperature=0.0,
        messages=[
            {"role": "system", "content": "Determine if the following query is out of scope for MTN customer support. Respond with 'out of scope' if it is, otherwise provide a response."},
            {"role": "user", "content": query}
        ]
    )
    
    # Interpret the model's response
    response = completion.choices[0].message
    
    if response == "out of scope":
        return "I'm sorry, but I can only assist with MTN-specific topics."  # Handle out of scope
    else:
        return generate_response(query, user_id)  # Generate response for in-scope queries