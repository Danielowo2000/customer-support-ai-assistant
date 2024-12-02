from flask import Flask, request, jsonify
from assistant.assistant_service import handle_audio_from_user

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the API!"

@app.route('/api/audio-message', methods=['POST'])
async def ask():  # Make the function asynchronous
    user_id = request.form.get('user_id')  # Get the user's ID from the form data
    audio_file = request.files['audio']  # Get the audio file from the form data
    response, category = await handle_audio_from_user(audio_file, user_id)  # Await the coroutine
    # Extract the content from the response and category
    category_content = category.content if hasattr(category, 'content') else str(category)

    return jsonify({'response': response, 'class': category_content})  # Return the response and class as JSON

if __name__ == "__main__":
    app.run(debug=True)  

