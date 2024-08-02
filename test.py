from llama_cpp import Llama
from dateparser import parse
import json


llm = Llama(
    model_path="models/ggml-model-f16.gguf",
    n_gpu_layers=-1
)
# dateparser無法正確辨識後天
prompt = """
Q: 請根據提供的內容，找出時間、地點、會議目的，並以給定格式輸出。請確保：
1. 使用引號來標記信息。
2. 使用冒號與類別作關聯。
3. 時間應保持相對時間的形式，並將它轉換成英文與24小時制。例如：
    - "tomorrow hh:mm"
    - "yesterday hh:mm"
    - "today hh:mm"
    - "the day after tomorrow hh:mm"
    - "the day before yesterday hh:mm"
    - "next Monday hh:mm"
4. 不需要對結果進行解釋。

格式：{ "time" : ["請在這裡輸入時間"], "location" : ["請在這裡輸入地點"], "purpose" : ["請在這裡輸入目的"] }
這是需要解析的內容："明天早上 8 點與後天下午 6 點，我們將在會議室 A 討論新產品的發佈計劃。"

\n\rA:
"""

output = llm(
    prompt=prompt,
    max_tokens=None,
    stop=["Q:"],
    echo=True
)
print("output:",output, "\n")
result = output['choices'][0]['text']
answer = result.split("\n\rA:")[1]
print("answer:",answer, "\n")
answer = json.loads(answer)
times_list = answer['time']
print("times_list:",times_list)

for times in times_list:
    print(times)
    absolute_time = parse(times, settings={'TIMEZONE': 'Asia/Taipei'})
    print("absolute_time:",absolute_time)
