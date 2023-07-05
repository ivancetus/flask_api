from pytube.exceptions import RegexMatchError

from youtube_download import get_yt
from flask import Flask, request, send_file, render_template, Response
from flask_cors import CORS
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
cors = CORS(app, expose_headers='Content-Disposition', resources={r'/': {'origins': '*'}})


@app.route('/', methods=['POST'])
def yt():
    data = request.get_json()
    print(data)
    youtube_url = data['url']
    file_format = data['format']
    logging.info(f'Processed json request: {data}')
    try:
        file_path = get_yt(youtube_url, file_format)
        if file_path:
            return send_file(file_path, mimetype='audio/mpeg', as_attachment=True)
        else:
            return Response(response="video not found, make sure url is correct", status=400)
    except RegexMatchError as e:
        logging.error(f'RegexMatchError: {str(e)}')
        if str(e).startswith('get_throttling_function_name'):
            return Response(response="something went wrong, server need to be updated, contact Ivan!", status=503)
        else:
            return Response(response=str(e) + " ,contact Ivan!", status=500)
    except Exception as e:
        logging.error(f'Error occurred: {str(e)}')
        if str(e).startswith('HTTP Error 429: Too Many Requests'):
            return Response(response="server ip blocked by YouTube, please try again later", status=503)
        else:
            return Response(response="server unavailable, contact Ivan!", status=500)


@app.route('/', methods=['GET'])
def info():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
