from dotenv import load_dotenv
import os
import openai
import pandas as pd 
import requests

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#1.上傳檔案================================================================
# script_directory = os.path.dirname(os.path.abspath(__file__))
# test_jsonl_path = os.path.join(script_directory, "test.jsonl")
# exam_jsonl_path = os.path.join(script_directory, "exam.jsonl")

# openai.File.create(
#     file=open(test_jsonl_path, "rb"),
#     purpose='fine-tune'
# )

# openai.File.create(
#     file=open(exam_jsonl_path, "rb"),
#     purpose='fine-tune'
# )

# print(openai.File.list())
#2.執行Validation================================================================

# training_file_id = "file-Yg5WQSrJr4PGQzXt82RuDwki"
# validation_file_id = "file-Ho8sNvdTPnbmfwpyDd9ZI3EB"

# Fine-tuning code
# openai.FineTune.create(
#     training_file= training_file_id,
#     validation_file = validation_file_id,
#     model="davinci:ft-personal:test1-2023-08-03-11-55-27",
#     suffix="validation_model"
# )

# print(openai.FineTune.list())
#3.確認Validation狀態================================================
fine_tuning_id ="ft-irNqlZd1c5cRHnb8eauayZo8"
response = openai.FineTune.retrieve(fine_tuning_id)
print(response)
print("Fine-tuning Status:", response.status)
#4.確認benchmark結果================================================================
file_id = "file-KfCpn7lguzALJjKPfHoZvT1r"
response = openai.File.download(file_id)
print(response)

with open('compiled_results.csv', 'wb') as file:
    file.write(response)
print("CSV file saved successfully.")

#print(result)