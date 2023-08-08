import openai
import os
import pandas as pd

openai.organization = os.getenv("OPENAI_API_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")


def benchmark(contextInjection, inputData, finetunedModelId):
    training_file_id = contextInjection
    validation_file_id = inputData
    
    #進行validation
    validation_response = openai.FineTune.create(
        training_file=training_file_id,
        validation_file=validation_file_id,
        model=finetunedModelId,
        suffix="validation_model"
    )
    #確認Validation結果
    fine_tune_id = validation_response['id']
    response = openai.FineTune.retrieve(fine_tune_id)
    print("Validation Status:", response["status"])
    #讀取validation結果
    csv_file_id = response.result_files[0]["id"]
    file_response = openai.File.download(csv_file_id)
    #將validation的result_files轉換成dataframe
    response_str = file_response.decode('utf-8')
    lines = response_str.strip().split('\n')
    header = lines[0].split(',')
    data = [dict(zip(header, line.split(','))) for line in lines[1:]]
    df = pd.DataFrame(data)
    print(df)

   
if __name__ == "__main__":
    contextInjection = "your_training_file_id" 
    inputData = "your_validation_file_id" 
    finetunedModelId = "your_finetuned_model_id"
    benchmark(contextInjection, inputData, finetunedModelId)

