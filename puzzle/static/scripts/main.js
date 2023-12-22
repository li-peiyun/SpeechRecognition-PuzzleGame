// 录音及语音处理
document.addEventListener('DOMContentLoaded', function () {
    // 获取页面中的元素
    const recordButton = document.getElementById('recordButton');
    const puzzleQuestionDiv = document.getElementById('puzzle_question');
    const puzzleAnswerDiv = document.getElementById('puzzle_answer');


    // 海龟汤内容
    let puzzleQuestionContent = puzzleQuestionDiv.innerHTML;
    let puzzleAnswerContent = puzzleAnswerDiv.innerHTML;

    // 用于存储录音数据的变量
    let mediaRecorder;
    let chunks = [];

    // 标记是否正在录音的变量
    let isRecording = false;

    // 添加点击按钮时的事件监听器
    recordButton.addEventListener('click', toggleRecording);

    // 切换录音状态的函数
    async function toggleRecording() {
        if (!isRecording) {
            // 如果当前没有录音，则开始录音
            startRecording();
        } else {
            // 如果当前正在录音，则停止录音
            stopRecording();
        }
    }

    // 开始录音的函数
    async function startRecording() {
        // 获取用户麦克风的音频流
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // 创建MediaRecorder对象，用于录音
        mediaRecorder = new MediaRecorder(stream);

        // 当有音频数据可用时触发该事件
        mediaRecorder.ondataavailable = (event) => {
            if (event.data.size > 0) {
                chunks.push(event.data);
            }
        };

        // 当录音停止时触发该事件
        mediaRecorder.onstop = () => {
            // 创建包含所有录音数据的Blob对象
            const blob = new Blob(chunks, { type: 'audio/wav' });

            // 生成录音的音频URL
            const audioUrl = URL.createObjectURL(blob);

            // 发送语音数据到后端
            sendAudioData(blob);

            // 重置 chunks 数组
            chunks = [];
        };

        // 开始录音
        mediaRecorder.start();

        // 更新按钮文本和状态
        recordButton.innerText = '停止录音';
        isRecording = true;
    }

    // 停止录音的函数
    function stopRecording() {
        // 停止录音
        mediaRecorder.stop();

        // 更新按钮文本和状态
        recordButton.innerText = '开始录音';
        isRecording = false;
    }

    // 发送语音数据到后端的函数
    function sendAudioData(blob) {
        // 创建FormData对象，用于将数据发送到后端
        const formData = new FormData();
        formData.append('audio', blob);
        formData.append('puzzle_question', puzzleQuestionContent);
        formData.append('puzzle_answer', puzzleAnswerContent);

        // 使用jQuery发送POST请求
        $.ajax({
            type: 'POST',
            url: '/process_audio', // 后端处理语音的路由
            data: formData,
            contentType: false,
            processData: false,
            success: function (response) {
                console.log('success');

                console.log('问题：'+response.question+'，回答：'+response.answer)
                // 将 response.question 放入发送的输入
                insertMessage(response.question);

                // 将 response.answer 放入返回的消息
                fakeMessage(response.answer);
                },
                error: function (error) {
                    console.error(error); // 处理失败后的回调函数
                }
        });
    }
});


// 显示谜底
document.getElementById('showAnswerButton').addEventListener('click', function() {
    var answerDiv = document.getElementById('answer');
    answerDiv.style.display = 'block';
    // 禁用按钮
    this.disabled = true;
    fakeMessage("请查看汤面看看你的想法是否正确吧！");
    document.getElementById('recordButton').disabled = true;
});

// 结束后返回到上一个界面
document.getElementById('end_up').addEventListener('click', function() {
  window.history.back();
});


//puzzle详情页样式逻辑
var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(document).ready(function() {

    setTimeout(function() {
        fakeMessage('现在你可以开始问问题啦！');
    }, 100);
});

function updateScrollbar() {
  var messagesContent = document.querySelector('.messages-content');
  messagesContent.scrollTop = messagesContent.scrollHeight;
}
function insertMessage(msg) {
    if ($.trim(msg) === '') {
        return false;
    }
    $('<div class="message message-personal">' + msg + '</div>').appendTo($('.messages-content')).addClass('new');
    updateScrollbar();

}



function fakeMessage(msg) {
    if ($('.message-input').val() !== '') {
        return false;
    }
    $('<div class="message loading new"><figure class="avatar"><img src="../static/images/avatar1.jpg" /></figure><span></span></div>').appendTo($('.messages-content'));
    updateScrollbar();

    setTimeout(function() {
        $('.message.loading').remove();
        $('<div class="message new"><figure class="avatar"><img src="../static/images/avatar1.jpg" /></figure>' + msg + '</div>').appendTo($('.messages-content')).addClass('new');
        updateScrollbar();
        i++;
    }, 1000 + (Math.random() * 20) * 100);
}
