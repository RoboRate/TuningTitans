import openai
import json
from dotenv import load_dotenv
import os


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generateAnswers(dataset_path, model_name):
    questions = []
    model_answer = []
    ideal_answer = []
    #將資料集的prompt和completion分開
    with open(dataset_path, "r", encoding="utf-8") as jsonl_file:
        for line in jsonl_file:
            entry = json.loads(line)
            prompt = entry["prompt"]
            expected_completion = entry["completion"].strip()

            #讓fine-tuning model回答prompt
            completion_request_kwargs = dict(
                model=model_name,
                prompt=prompt+ '\n\n###\n\n',
                max_tokens=50,
                temperature=1,
            )
            #得到fine-tuning model的回答
            response = openai.Completion.create(**completion_request_kwargs)
            predicted_completion = response.choices[0].text.strip()

            questions.append(prompt)
            model_answer.append(predicted_completion)
            ideal_answer.append(expected_completion)

    cust_prod_info = {
        'Question': questions,
        'YourModelAnswer': model_answer,
        'IdealAnswer':ideal_answer
    }
    return cust_prod_info

def getCompletionFromMessages(messages, model="gpt-3.5-turbo-16k", temperature=1, max_tokens=13000):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens, #This model's maximum context length is 16385 tokens.
    )
    return response.choices[0].message["content"]


def evalWithRubric(test_set):
    questions = test_set['Question']
    yourmodelanswer = test_set['YourModelAnswer']
    idealanswer = test_set['IdealAnswer']
    system_message = """\
    你是一個評分的老師，請透過學生的實際回答與標準回答的內容比較來做評估，評估學生是否有回答相對應的答案。\
    評估學生實際回答問題的表現。
    """

    user_message = f"""\
    你正在針對問題來做學生的實際回答以及標準回答間的差異評分，並且依照評分邏輯做為判斷邏輯。
    以下是數據：
    [評分資料開始]
    ************
    [問題]: {questions}
    ************
    [學生的實際回答]: {yourmodelanswer}
    ************
    [標準回答]: {idealanswer}
    ************
    [評分邏輯]：
    1. 將學生針對問題的實際回答與標準回答進行比較，忽略風格、語法、順序或標點的差異。
    2. 對於提出的問題，評估學生是否有回答相對應的答案，並且將學生的實際回答與標準回答進行比較。
    3. 實際回答可能是標準回答的子集或超集，或者可能與標準回答有衝突。
    [評分資料結束]
    請你確定下方哪種情況適用，給予每個回答分數(最低0分，最高10分)，並且回覆一個數字：
    (0分)實際回答跟標準回答沒有任何交集。
    (1~3分)實際回答只包含部分標準回答內容。
    (4~6分)實際回答大部分包含標準回答。
    (7~10分)實際回答與標準回答的內容相符。

    請將你以上各問題的評分，以以下格式輸出：
    問題1：（輸出一個數字）
    問題2：（輸出一個數字）
    ...
    問題N：（輸出一個數字）
    總分數：（加總上述問題的分數，並輸出一個數字）
    題目數：(輸出一個數字)
"""

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message}
    ]

    response = getCompletionFromMessages(messages)
    return response

if __name__ == "__main__":
    dataset_path = "C:\\Users\\Sherry Wu\\.vscode\\Roborate_OpenAI\\QA.jsonl"
    model_names = ["davinci:ft-personal-2023-08-14-07-08-20", "davinci"]

    for model_name in model_names:
        result = generateAnswers(dataset_path, model_name)
        print(f"Results for model: {model_name}")
        print(result)

        evaluation_output = evalWithRubric(result)
        print(f"Evaluation output for model: {model_name}")
        print(evaluation_output)

#     result = generateAnswers(dataset_path, model_name)
#     print(result)
    # with open("result.json", "w", encoding="utf-8") as result_file:
    #     json.dump(result, result_file, ensure_ascii=False, indent=4)
# evaluation_output = evalWithRubric(result)
# print(evaluation_output)
# with open("evaluation_output.json", "w", encoding="utf-8") as eval_output_file:
#     json.dump(evaluation_output, eval_output_file, ensure_ascii=False, indent=4)