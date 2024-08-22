from llama_cpp import Llama
from dateparser import parse
import re
import json
import time


llm = Llama(
    model_path="models\ggml-llama3-1-8b-f16.gguf", # put the path to the model here
    n_gpu_layers=0
)

def get_LLM_response(message):
    prompt = f"""
    Q: 請根據提供的內容，找出詳細的時間、地點、會議目的，並以給定格式輸出。請確保：
    1. 格式為json格式。
    2. 時間應保持相對時間的形式，並將它轉換成英文與24小時制。
    3. 只需要輸出格式以及他的答案就好。
    4. 如果有多個時間，請全部列出在"time"，並將每個時間以開始時間、結束時間的形式呈現，請注意，如果只有一個時間，則列出來的開始時間與結束時間應相同。
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
    #print("match_text", match_text)
    print("answer:",answer, "\n")
    answer = json.loads(answer)
    times_list = answer['time']
    print("times_list:",times_list)
    
    return answer

print(get_LLM_response("會議時間是明天下午2點到4點以及後天早上8點，地點在台北市信義區，目的是討論公司業務。"))
