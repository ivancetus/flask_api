from youtube_download import get_yt
from flask import Flask, request, send_file
from flask_cors import CORS
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
cors = CORS(app, expose_headers='Content-Disposition', resources={r'/': {'origins': '*'}})


@app.route('/', methods=['POST'])
def yt():
    file_path = ""
    data = request.get_json()
    print(data)
    youtube_url = data['url']
    file_format = data['format']
    logging.info(f'Processed json request: {data}')
    try:
        file_path = get_yt(youtube_url, file_format)
    except Exception as e:
        logging.error(f'Error occurred: {str(e)}')
    if not file_path:
        response = "bad request!", 400
    else:
        response = send_file(file_path, mimetype='audio/mpeg', as_attachment=True)
    return response


@app.route('/test')
def test():
    return "request made"


if __name__ == '__main__':
    app.run()
