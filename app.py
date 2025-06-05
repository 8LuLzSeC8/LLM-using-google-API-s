from datetime import datetime
from google.cloud import speech
from google.protobuf import wrappers_pb2
from google.cloud import texttospeech_v1
from flask import Flask, flash, render_template, request, redirect, url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from google.cloud import language_v2

import os
import os
import google.generativeai as genai

os.environ["GEMINI_API_KEY"] = "Your Key Here"
genai.configure(api_key=os.environ["GEMINI_API_KEY"])



os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "serv_account.json"


def upload_to_gemini(path, mime_type=None):
  """Uploads the given file to Gemini.

  See https://ai.google.dev/gemini-api/docs/prompting_with_media
  """
  file = genai.upload_file(path, mime_type=mime_type)
  print(f"Uploaded file '{file.display_name}' as: {file.uri}")
  return file

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[]
)

client = texttospeech_v1.TextToSpeechClient()

def sample_synthesize_speech(text=None, ssml=None):
    input = texttospeech_v1.SynthesisInput()
    if ssml:
      input.ssml = ssml
    else:
      input.text = text

    voice = texttospeech_v1.VoiceSelectionParams()
    voice.language_code = "en-US"
    # voice.ssml_gender = "MALE"

    audio_config = texttospeech_v1.AudioConfig()
    audio_config.audio_encoding = "LINEAR16"

    request = texttospeech_v1.SynthesizeSpeechRequest(
        input=input,
        voice=voice,
        audio_config=audio_config,
    )

    response = client.synthesize_speech(request=request)

    return response.audio_content


app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configure tts folder
TTS_FOLDER = 'tts_results'
app.config['TTS_FOLDER'] = TTS_FOLDER

os.makedirs(TTS_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_files():
    files = []
    for filename in os.listdir(UPLOAD_FOLDER):
        if allowed_file(filename):
            files.append(filename)
            print(filename)
    files.sort(reverse=True)
    return files

def get_tts_files():
    tts_files = []
    for filename in os.listdir(TTS_FOLDER):
        if allowed_file(filename):
            tts_files.append(filename)
            print(filename)
    tts_files.sort(reverse=True)
    return tts_files


@app.route('/')
def index():
    files = get_files()
    tts_files = get_tts_files()
    return render_template('index.html', files=files, tts_files = tts_files)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'audio_data' not in request.files:
        flash('No audio data')
        return redirect(request.url)
    file = request.files['audio_data']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        # filename = secure_filename(file.filename)
        filename = datetime.now().strftime("%Y%m%d-%I%M%S%p") + '.wav'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        fpath = 'uploads/'+filename

        input_files = [upload_to_gemini(fpath, mime_type="audio/wav"),]
        response = chat_session.send_message(["please transcribe and provide sentiment analysis like this:\nTranscription: output of transcription here\nsentiment: sentiment analysis output here in one word",input_files[0]])
        new_fpath = fpath+'.txt'
        f = open(new_fpath,'w')
        f.write(response.text)
        f.close()

        wav = sample_synthesize_speech(response.text)
        fname = filename
        fpath = os.path.join(app.config['TTS_FOLDER'], fname)
        f = open(fpath,'wb')
        f.write(wav)
        f.close()



    return redirect('/') #success

@app.route('/upload/<filename>')
def get_file(filename):
    return send_file(filename) 

@app.route('/script.js',methods=['GET'])
def scripts_js():
    return send_file('./script.js')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/tts_results/<filename>')
def tts_file(filename):
    return send_from_directory(app.config['TTS_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)