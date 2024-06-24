import librosa
import numpy as np
from scipy.signal import find_peaks
from vosk import Model, KaldiRecognizer
import json
import os
from django.conf import settings
import warnings

vosk_model_path = os.path.join(settings.BASE_DIR, 'models', 'vosk-model-small-en-us-0.15')

warnings.filterwarnings('ignore', category=FutureWarning)

def analyze_audio(file_path):
  
  try:
    y, sr = librosa.load(file_path, sr=None)
  except Exception as e:
    print(f"Failed to load audio file {file_path}: {str(e)}")
    return None, None
  features = extract_features(y, sr)
  voice_pattern_changes = detect_voice_pattern_changes(y, sr)
  slurred_speech = detect_slurred_speech(y, sr)
  interaction_ability = assess_interaction_ability(file_path)
  
  result = {
    'features': features,
    'voice_pattern_changes': voice_pattern_changes,
    'slurred_speech': slurred_speech,
    'interaction_ability': interaction_ability
  }
  
  user_friendly_result = describe_results(result)

  return user_friendly_result

def extract_features(y, sr):
  mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
  return mfccs.mean(axis=1).tolist()

def detect_voice_pattern_changes(y, sr):
  energy = librosa.feature.rms(y=y)[0]
  peaks, _ = find_peaks(energy, height=np.max(energy) * 0.5)
  return len(peaks)

def detect_slurred_speech(y, sr):
  tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
  return 'Slurred' if tempo < 80 else 'Clear'

def assess_interaction_ability(file_path):
  model = Model(vosk_model_path)
  rec = KaldiRecognizer(model, 16000)
  interaction_text = ''

  with open(file_path, "rb") as f:
      while True:
          data = f.read(4000)
          if len(data) == 0:
              break
          if rec.AcceptWaveform(data):
              result = json.loads(rec.Result())
              interaction_text += result.get('text', '')

  return {
      'text': interaction_text,
      'interaction_level': 'Good' if len(interaction_text) > 10 else 'Poor'
  }

def describe_results(result):
    features_description = describe_features(result['features'])
    voice_pattern_description = describe_voice_pattern(result['voice_pattern_changes'])
    speech_clarity_description = describe_speech_clarity(result['slurred_speech'])
    interaction_assessment_description = describe_interaction_ability(result['interaction_ability'])

    return {
        'speech_summary': features_description,
        'voice_pattern_description': voice_pattern_description,
        'speech_clarity': speech_clarity_description,
        'interaction_assessment': interaction_assessment_description
    }

def describe_features(features):
    # Simplified example of feature description
    tone_description = "moderately varied" if np.std(features) > 10 else "relatively flat"
    return f"The speech analysis reveals a {tone_description} tone and pitch, suggesting a lively conversation."

def describe_voice_pattern(voice_pattern_changes):
    if voice_pattern_changes > 20:
        return f"The speaker had {voice_pattern_changes} noticeable changes in voice pattern, indicating a very dynamic speech style."
    elif voice_pattern_changes > 10:
        return f"The speaker had {voice_pattern_changes} noticeable changes in voice pattern, indicating a dynamic speech style."
    else:
        return f"The speaker had {voice_pattern_changes} noticeable changes in voice pattern, indicating a relatively steady speech style."

def describe_speech_clarity(slurred_speech):
    if slurred_speech == "Slurred":
        return "The speech was detected to be slurred, which could indicate tiredness or difficulty in speaking clearly."
    else:
        return "The speech was detected to be clear and well-articulated."

def describe_interaction_ability(interaction_ability):
    text = interaction_ability.get('text', '')
    interaction_level = interaction_ability.get('interaction_level', 'Poor')

    if interaction_level == 'Good':
        return {
            'recognized_text': text,
            'interaction_quality': "The speaker communicated effectively, showing good interaction skills."
        }
    else:
        return {
            'recognized_text': text,
            'interaction_quality': "The speaker's communication was limited, suggesting potential difficulties in interacting."
        }