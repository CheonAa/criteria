import openai
import json
from flask import Flask, request, make_response
from slack_sdk import WebClient
 

openai.api_key = "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" # YOUR_API_KEY에 발급받은 API key를 입력하세요.
model_engine = "text-davinci-003" # GPT 모델 엔진을 설정해줍니다.

token = "xoxb-6140418851830-6149620358327-dk9giUgRquLQmnjm5WkTIGkJ"
app = Flask(__name__)
client = WebClient(token)
 

# 답변 생성하는 부분
def get_answer(text):

    if "사과" in text:
        return "바나나"
 
    prompt = f"Q: {text}\nA:"
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

 
 
 # 슬랙에서 메세지 받아오는 부분
def event_handler(event_type, slack_event):
    channel = slack_event["event"]["channel"]
    string_slack_event = str(slack_event)
    
    if string_slack_event.find("{'type': 'user', 'user_id': ") != -1:
        try:
            if event_type == 'app_mention':
                user_query = slack_event['event']['blocks'][0]['elements'][0]['elements'][1]['text']
                answer = get_answer(user_query)
                result = client.chat_postMessage(channel=channel, text=answer)
            return make_response("ok", 200, )
        except IndexError:
            pass
 
    message = "[%s] cannot find event handler" % event_type
 
    return make_response(message, 200, {"X-Slack-No-Retry": 1})
 

@app.route('/', methods=['POST','GET'])
def hello_there():
    
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
 
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("There are no slack request events", 404, {"X-Slack-No-Retry": 1})
 
 
if __name__ == '__main__':
    app.run(debug=True, port=5002)