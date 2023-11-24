import ast

from flask import Flask, render_template, request, jsonify
from aip import AipSpeech
import subprocess
import tempfile

APP_ID = '43554036'
API_KEY = '6KGm6tAxGK6ooLkLODnxTEvH'
SECRET_KEY = 'woFwxbwL3oa2fRzX5lIjk4fKqLhwje3p'
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



# 音频处理
@app.route('/process_audio', methods=['POST'])
def process_audio():
    # 接收汤面内容
    puzzle_question = request.form.get('puzzle_question')
    # 接收汤底内容
    puzzle_answer = request.form.get('puzzle_answer')
    # 接收音频文件
    audio_file = request.files.get('audio')
    # 可以识别内容，形式错误
    # audio_content = audio_file.read()

    # 创建临时文件并保存上传的音频文件
    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
        temp_audio_path_original = temp_audio_file.name
        audio_file.save(temp_audio_path_original)

    # 使用 FFmpeg 进行音频格式转换
    temp_audio_path_converted = tempfile.NamedTemporaryFile(delete=False).name
    subprocess.run([ffmpeg_path, '-y', '-i', temp_audio_path_original, '-f', 's16le', '-ac', '1', '-ar', '16000', temp_audio_path_converted])


    # 读取转换后的音频文件内容
    with open(temp_audio_path_converted, 'rb') as converted_file:
        audio_content = converted_file.read()

    #####################################
    # 在这里处理接收到的语音文件
    #####################################
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 使用文件路径调用百度地图API
    question_result = client.asr(audio_content, 'wav', 16000, {'dev_pid': 1537})
    # 查看结果形式
    # print(question_result)
    # 构建包含处理结果的字典对象
    result = {
        # 处理完成后需要替换以下内容
        # xwt替换question内容为检测的句子
        'question': question_result['result'][0],
        # lx替换answer内容为chatgpt回答
        'answer': '不是'
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
