from flask import Flask, render_template
from flask_socketio import SocketIO
import threading
from speech import start_listening

app = Flask(__name__)
app.config['SECRET_KEY'] = 'captions123'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

def on_caption(text):
    print(f"Emitting: {text}")
    socketio.emit('caption', {'text': text})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    thread = threading.Thread(
        target=start_listening,
        args=(on_caption,),
        daemon=True
    )
    thread.start()
    socketio.run(app, debug=False, host='0.0.0.0', port=5000, 
                 allow_unsafe_werkzeug=True)