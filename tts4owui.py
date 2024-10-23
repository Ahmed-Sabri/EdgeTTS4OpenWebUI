from flask import Flask, request, jsonify, send_file
import edge_tts
import os
import asyncio

app = Flask(__name__)

@app.route('/tts/audio/speech', methods=['POST'])
async def tts_audio_speech():
    try:
        data = request.json
        print(f"Received data: {data}")  # Log incoming data
        text = data.get('input', '')  # Change 'text' to 'input'
        voice = data.get('voice', 'en-US-EmmaMultilingualNeural')  # Get voice, default if not provided
        
        if not text:
            return jsonify({"success": False, "error": "No text provided"}), 400

        tts = edge_tts.Communicate(text, voice)  # Use the provided voice
        output_file = "output.mp3"
        await tts.save(output_file)  # Await the save method

        return send_file(output_file, mimetype="audio/mpeg")
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
