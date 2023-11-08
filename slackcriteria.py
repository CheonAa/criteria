import requests
import pandas as pd

def get_csv_data(event):
    # github에서 csv 파일을 가져옵니다.
    url = "https://api.github.com/repos/CheonAa/criteria/slackcriteria.py"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content
    else:
        raise Exception("데이터를 가져올 수 없습니다.")

    # csv 파일의 내용을 Pandas DataFrame으로 변환합니다.
    df = pd.read_csv(io.BytesIO(data))

    # slash command에서 키워드를 가져옵니다.
    keyword = event['text'].split()[1]

    # 키워드가 포함된 행만 추출합니다.
    filtered_df = df[df['성취기준명'].str.contains(keyword)]

    # 성취기준 코드와 성취기준명을 출력합니다.
    for index, row in filtered_df.iterrows():
        event.reply(f"{row['성취기준 코드']}: {row['성취기준명']}")

app.on("/성취기준", get_csv_data)