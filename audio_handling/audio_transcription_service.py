from openai import OpenAI
client = OpenAI()

def convert_audio_to_text(local_input_file_path: str) -> dict:
    file = open(local_input_file_path, 'rb')
    transcription = client.audio.transcriptions.create(model="whisper-1", file =file)
    print(transcription.text)
    return transcription.text

