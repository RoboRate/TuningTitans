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

    print(response)
    return response

def getModelAnalysis(modelResultFileId): #取得分析結果
    url = f'https://api.openai.com/v1/files/{modelResultFileId}/content'
    headers = {"Authorization": f'Bearer {openai.api_key}'}
    response = requests.get(url, headers=headers)
    
    app_root = os.path.dirname(os.path.abspath(__file__))
    temp_folder = os.path.join(app_root, "ModelAnalysis")

    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    
    return response.text