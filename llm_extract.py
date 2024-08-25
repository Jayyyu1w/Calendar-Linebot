from llama_cpp import Llama
from dateparser import parse
import re
import json
import time


llm = Llama(
    model_path="models\ggml-llama3-1-8b-f16.gguf", # put the path to the model here
    n_gpu_layers=0
)

def get_LLM_response(message: str):
    prompt = f"""
    Q: 請根據提供的內容，找出詳細的時間、地點、會議目的，並以給定格式輸出。請確保：
    1. 格式為json格式。
    2. 時間應保持相對時間的形式，並將它轉換成英文與24小時制。
    3. 只需要輸出格式以及他的答案就好。
    4. 請提取出文字內的所有時間，並全部放在"time"的list內，且每個時間應包含開始時間與結束時間。如果文字中只有一個時間，請將開始與結束時間設置為相同。確保日期和時間以"開始日期 開始時間"和"結束日期 結束時間"的形式列出。
    以下為給定的格式：
    {{ "time" : ["開始日期 開始時間", "結束日期 結束時間"], "location" : ["請在這裡輸入地點"], "purpose" : ["請在這裡輸入目的"] }}
    這是需要解析的內容：
    "{message}"
    目前的日期為："{time.strftime('%Y-%m-%d')}"
    \n\rA:
    """

    output = llm(
        prompt=prompt,
        max_tokens=None,
        stop=["Q:", "\n\rA:", "A:", "\rA:"],
        echo=True
    )
    print("output:",output, "\n")
    result = output['choices'][0]['text']

    result = result.replace("\n", "")
    match_text = re.search(r'\rA:\s*(\{.*?\})', result)
    match_text = match_text.group(1)
    answer = match_text.replace("\rA:", "")
    # 使用正則表達式找到所有的 "time" 部分並將它們提取出來
    time_matches = re.findall(r'"time" : (\[.*?\])', answer)
    # 將所有的時間範圍合併成一個列表
    combined_times = '[' + ', '.join(time_matches) + ']'

    time_matches = re.findall(r'"time"\s*:\s*(\[[^\]]*\])', answer)
    combined_times = '[' + ', '.join(time_matches) + ']'
    answer = re.sub(r'"time"\s*:\s*\[[^\]]*\]\s*,?', '', answer)
    answer = '{ "time" : ' + combined_times + ',' + answer.lstrip('{').rstrip(' }') + ' }'
    print("answer:",answer, "\n")
    answer = json.loads(answer)
    print(type(answer["purpose"]))
    print(answer["purpose"][0])
    
    return answer
