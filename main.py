from flask import Flask, request, json
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
app = Flask(__name__)

class Summarizer:
    def __init__(self, text) -> None:
        self.text = text

    def getSummary(self) -> str:
        summarizer = pipeline("summarization", model="stevhliu/my_awesome_billsum_model")
        return summarizer(self.text)[0]['summary_text']
        

@app.route('/getsummary', methods=['POST'])
def getSummary():
    req = request.get_json()
    vid_id = req['vid_id']

    data = YouTubeTranscriptApi.get_transcript(vid_id)

    transcript = ""
    for obj in data:
        transcript += obj['text'] + " "

    transcript = transcript.replace('\n', ' ')
    transcript = transcript[0:3000]

    return json.jsonify({
        'summary' : Summarizer(transcript).getSummary()
    })

while True:
    app.run(debug=True)