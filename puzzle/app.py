import ast
from flask import Flask, render_template, request, jsonify

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
    # 接收音频文件
    audio_file = request.files['audio']

    #####################################
    # 在这里处理接收到的语音文件
    #####################################

    # 构建包含处理结果的字典对象
    result = {
        # 处理完成后需要替换以下内容
        # xwt替换question内容为检测的句子
        'question': '男人死了吗？',
        # lx替换answer内容为chatgpt回答
        'answer': '不是'
    }

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
