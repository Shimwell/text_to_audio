
import os

from google.cloud import texttospeech
import argparse

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="google_secret_keys.json"


parser = argparse.ArgumentParser(
)
parser.add_argument('-i', '--input',
                    default='input_ssml_text.html',
                    help='input file in SSML format')
parser.add_argument('-o', '--output',
                    default='output.mp3',
                    help='output file in mp3L format')

args = parser.parse_args()

def synthesize_ssml_file(ssml_file, mp3_file):
    """Synthesizes speech from the input file of ssml.

    Note: ssml must be well-formed according to:
        https://www.w3.org/TR/speech-synthesis/
    """

    client = texttospeech.TextToSpeechClient()

    with open(ssml_file, "r") as f:
        ssml = f.read()
        input_text = texttospeech.SynthesisInput(ssml=ssml)

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        language_code="en-UK",
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=input_text,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(mp3_file, "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file', mp3_file)


if __name__ == "__main__":
    synthesize_ssml_file(args.input, args.output)
