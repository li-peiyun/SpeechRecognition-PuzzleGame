import ast
from flask import Flask, render_template, request, jsonify
import subprocess
import tempfile
from chatgpt_answer import generate_response
from iat_ws_python3 import *

APP_ID = 'c0c8e7d0'  # 请替换为您的科大讯飞 APP ID
API_KEY = '2062a1183a98296cad37d4b4265452ad'  # 请替换为您的科大讯飞 API Key
SECRET_KEY = 'NmNiZjFiM2E2OTc5MWVjZDM0OWQzNTY4'  # 请替换为您的科大讯飞 API Secret

ffmpeg_path = 'D:/AAAProgramFiles/ffmpeg-2023-11-22-git-0008e1c5d5-full_build/bin/ffmpeg'

app = Flask(__name__)


# 欢迎页
@app.route('/')
def index():
    return render_template("index.html")


# 选择页
@app.route('/selection')
def selection_page():
    import dbutil
    db = dbutil.dbUtils('puzzle.db')  # 链接数据库
    sql = 'select * from puzzle'
    puzzle_list = db.db_action(sql, 1)  # 查询并返回谜题列表
    db.close()  # 关闭数据库
    return render_template("selection.html", data=puzzle_list)  # 将数据传递到selection.html页面中


# 谜题页
@app.route('/puzzle/<detail>')
def puzzle_page(detail):
    puzzle = ast.literal_eval(detail)
    return render_template("puzzle.html", data=puzzle)


# 语音识别接口

# 音频处理
@app.route('/process_audio', methods=['POST'])
def process_audio():
    # 接收汤面内容
    puzzle_question = request.form.get('puzzle_question')
    # 接收汤底内容
    puzzle_answer = request.form.get('puzzle_answer')
    # 接收音频文件
    audio_file = request.files.get('audio')

    # 创建临时文件并保存上传的音频文件
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
        temp_audio_path_original = temp_audio_file.name
        audio_file.save(temp_audio_path_original)

    # 使用 FFmpeg 进行音频格式转换
    temp_audio_path_converted = tempfile.NamedTemporaryFile(delete=False).name
    subprocess.run([ffmpeg_path, '-y', '-i', temp_audio_path_original, '-f', 's16le', '-ac', '1', '-ar', '16000', temp_audio_path_converted])

    # 调用科大讯飞语音识别
    question = transfer(temp_audio_path_converted)
    response = '2'

    # chatgpt接口
    # response = generate_response(puzzle_answer, question)

    # 构建包含处理结果的字典对象
    result = {
        'question': question,
        'answer': response
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
