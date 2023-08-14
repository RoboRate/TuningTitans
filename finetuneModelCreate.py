import openai
import os
import requests

openai.api_key = os.getenv("OPENAI_API_KEY")

def modelCreate(**kwargs): #訓練模型，取得模型id
    training_file = kwargs.get("training_file")
    validation_file = kwargs.get("validation_file")
    model = kwargs.get("model")
    
    n_epochs = kwargs.get("n_epochs")
    print(f'n_epochs is {n_epochs}')
        
    batch_size = kwargs.get("batch_size")
    print(f'batch_size is {batch_size}')

    learning_rate_multiplier = kwargs.get("learning_rate_multiplier")
    print(f'learning_rate_multiplier is {learning_rate_multiplier}')
    
    requestBody = {
        "training_file": training_file,
        "validation_file": validation_file,
        "model": model,
    }
    
    if n_epochs:
        requestBody["n_epochs"]= n_epochs
    if batch_size:
        requestBody["batch_size"]= batch_size
    if learning_rate_multiplier:
        requestBody["learning_rate_multiplier"]= learning_rate_multiplier
    
    response = openai.FineTune.create(**requestBody)
    print(response)
    return {"fine_tuned_model": response["fine_tuned_model"], "id": response["id"], "status": response["status"]}

def modelStatusCheck(modelID): #取得已開始訓練的模型，是否已訓練完成的狀態
    response = openai.FineTune.retrieve(modelID)
    status = response['status']
    fine_tuned_model = response['fine_tuned_model']
    result_files = response['result_files'][0]['id']
    print(response)
    return {"fine_tuned_model":fine_tuned_model, "id": modelID, "status": status, "result_files": result_files}

def getModelAnalysis(modelResultFileId): 
    url = f'https://api.openai.com/v1/files/{modelResultFileId}/content'
    headers = {"Authorization": f'Bearer {openai.api_key}'}
    response = requests.get(url, headers=headers)
    fileName = modelResultFileId + "_modelAnalysis.csv" 
    with open(fileName, "w", encoding="UTF-8") as file:
        file.write(response.text)    
    return response.text

if __name__ == "__main__":
    #取得model狀態
    # davinciModelId = 'ft-bJsyVOAiV3lfmzrUGvPLGSUt'
    # response1 = modelStatusCheck(davinciModelId)
    # print('davinci model:')
    # print(response1)
    # print('================================')
        
    adaModelId = 'ft-l2tBUwUM9Kud4Z5lNgM0VYmB'
    response2 = modelStatusCheck(adaModelId)
    print('ada model:')
    print(response2)
    
    #已訓練完成的model，取得analysis結果
    model_result_file = 'file-hHXxpLipH6tkzJwPl916NnrM'
    response = getModelAnalysis(model_result_file)
