from flask import Flask, request, jsonify
import requests
import csv
import io

app = Flask(__name__)

# 슬랙 Slash Command 엔드포인트
@app.route('/search', methods=['POST'])
def search_csv():
    # 슬랙에서 보낸 키워드 받기
    keyword = request.form.get('text')

    # GitHub API를 사용하여 CSV 파일 내용 가져오기
    csv_url = 'https://github.com/CheonAa/criteria/blob/main/keywordlist.csv'  # GitHub의 Raw 파일 URL
    headers = {'Authorization': 'token YOUR_GITHUB_TOKEN'}
    response = requests.get(csv_url, headers=headers)
    
    # CSV 파싱
    csv_content = response.content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(csv_content))
    
    # 키워드로 검색
    results = []
    for row in csv_reader:
        if keyword in row['성취기준명']:
            results.append(f"코드: {row['성취기준 코드']}, 명: {row['성취기준명']}")
    
    # 슬랙 메시지 형식으로 응답 구성
    message = {
        "response_type": "in_channel",
        "text": "검색 결과입니다:",
        "attachments": [{"text": "\n".join(results)}]
    }

    return jsonify(message)

if __name__ == '__main__':
    app.run()
