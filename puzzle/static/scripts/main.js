// 录音及语音处理
document.addEventListener('DOMContentLoaded', function () {
    // 获取页面中的元素
    const recordButton = document.getElementById('recordButton');
    const resultDiv = document.getElementById('result');
    const dialogContainer = document.getElementById('dialog');
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

            ///////////////////////////////////
            // 在页面上显示录制的语音，测试用，后期删除
            ///////////////////////////////////
            const audioElement = document.createElement('audio');
            audioElement.controls = true;
            audioElement.src = audioUrl;
            resultDiv.innerHTML = '';
            resultDiv.appendChild(audioElement);

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

                // 创建新的 div 元素，显示新的对话
                const questionElement = document.createElement('div');
                questionElement.innerHTML = `问：${response.question}`;
                const answerElement = document.createElement('div');
                answerElement.innerHTML = `答：${response.answer}`;

                // 将新的对话添加到 dialogContainer 中
                dialogContainer.appendChild(questionElement);
                dialogContainer.appendChild(answerElement);
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
});