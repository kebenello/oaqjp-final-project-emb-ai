import requests
import json

def emotion_detector(text_to_analyze):
    """
    Analyzes the emotion of a given text using the Watson NLP Emotion Predict service.

    Args:
        text_to_analyze (str): The text to be analyzed.

    Returns:
        dict: A dictionary containing the emotion predictions, or an error message.
    """
    if not text_to_analyze or not text_to_analyze.strip():
        # The dominant emotion for a blank input is 'joy' with a high score.
        # To better reflect an empty input, we return a specific state.
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }

    try:
        response = requests.post(url, headers=headers, json=input_json)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the JSON response
        data = response.json()
        
        # Extract the emotion predictions
        emotion_predictions = data.get('emotionPredictions', [])[0].get('emotion', {})

        # Find the dominant emotion
        dominant_emotion = max(emotion_predictions, key=emotion_predictions.get)
        emotion_predictions['dominant_emotion'] = dominant_emotion

        return emotion_predictions

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}
    except (IndexError, KeyError) as e:
        return {"error": f"Could not parse emotion predictions from response: {e}"}

if __name__ == '__main__':
    # Example usage of the emotion_detector function
    text1 = "I am so happy to be learning about Natural Language Processing."
    text2 = "I am really sad about the news."
    text3 = "" # Blank input example

    print(f"Analyzing: '{text1}'")
    result1 = emotion_detector(text1)
    print(json.dumps(result1, indent=2))
    
    print("\n" + "="*50 + "\n")

    print(f"Analyzing: '{text2}'")
    result2 = emotion_detector(text2)
    print(json.dumps(result2, indent=2))

    print("\n" + "="*50 + "\n")

    print(f"Analyzing: Blank Input")
    result3 = emotion_detector(text3)
    print(json.dumps(result3, indent=2))

