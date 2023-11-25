import requests
import json

def generate_response(assistant_content, user_content):
    # 设置API端点和密钥
    api_endpoint = "https://api.openai.com/v1/chat/completions"
    api_key = "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"
    # 设置请求标头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # 设置请求数据
    data = {
        "model": "gpt-3.5-turbo",  # 指定模型
        "messages": [
            {"role": "system", "content": "这是一个猜谜游戏。用户只知道谜面，需要你根据谜底回答是或不是,并且只能回答是或不是，如果无法回答，就随机回答是或不是。"},
            {"role": "assistant", "content": assistant_content},
            {"role": "user", "content": user_content},
        ],
    }

    # 发送POST请求
    response = requests.post(api_endpoint, headers=headers, data=json.dumps(data))

    # 处理响应
    if response.status_code == 200:
        result = response.json()
        # 提取生成的文本
        generated_text = result["choices"][0]["message"]["content"]
        return generated_text
    else:
        return f"Error: {response.status_code} - {response.text}"

# 调用函数并打印生成的文本
# assistant_content = "《半瓶香水》谜底：我的妈妈前几天去世了，妈妈的去世对我产生了极大打击，以至于我产生了幻觉和梦游症，到了夜晚，梦游状态的我穿上妈妈生前给我买的漂亮衣服，喷上妈妈生前送我的香水，到她的墓地前和她聊天。那天我在照镜子时，把镜子里的自己幻想成了妈妈，我便与她理论，却不小心把镜子推倒了，镜子碎了一地，我赶忙用手去捡，手被玻璃割破，鲜血流了出来。"
# user_content = "我精神不正常吗？"
# generated_text = generate_response(assistant_content, user_content)
# print(generated_text)