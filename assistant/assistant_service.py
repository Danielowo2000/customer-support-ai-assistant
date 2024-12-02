from utils.file_utils import persist_binary_file_locally, create_unique_tmp_file
from transcoding.transcoding_service import convert_file_to_readable_mp3
from audio_handling.audio_transcription_service import convert_audio_to_text
from chat.chat_service import handle_get_response_for_user, generate_category
from audio_handling.eleven_labs_audio_generation_service import convert_text_to_audio


def __get_transcoded_audio_file_path(data: bytes) -> str:
    local_file_path = persist_binary_file_locally(data, file_suffix='user_audio.mp3')
    local_output_file_path = create_unique_tmp_file(file_suffix='transcoded_user_audio.mp3')
    convert_file_to_readable_mp3(
        local_input_file_path=local_file_path,
        local_output_file_path=local_output_file_path
    )
    return local_file_path


async def handle_audio_from_user(audio_file, user_id):
    # Read the contents of the audio file synchronously
    audio_data = audio_file.read()  # Read the file contents as bytes

    # Now pass the audio_data to the function that expects bytes
    transcoded_user_audio_file_path = __get_transcoded_audio_file_path(audio_data)
    transcript_content_text = convert_audio_to_text(transcoded_user_audio_file_path)
    text_content = transcript_content_text
    ai_text_reply = handle_get_response_for_user(text_content, user_id)
    category = generate_category(text_content)
    print("ai_text_reply>>", ai_text_reply)
    output_audio_local_file_path = convert_text_to_audio(ai_text_reply)
    return output_audio_local_file_path, category