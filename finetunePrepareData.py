import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")

file_path = 'testfile.jsonl'

def fileTransferToPreparedData(): 
    # 將原始Jsonl檔案，按照openai訓練模型要求，(使用CLI fine_tunes.prepare_data會給的建議)
    # (1) prompt的suffix加上" ->"，completion的suffix加上 "\n"
    # (2) prompt若有英文最好全為小寫
    # (3) completion的字串起首為一空格
    with open (file_path, "r", encoding="UTF-8") as file:
        content1 = file.readline()
        while content1:
            content2 = json.loads(content1.strip())
            
            prompt = content2['prompt']
            completion = content2['completion']
            completion = completion.lower()
            
            promptModified = prompt + ' ->'
            completionModified = ' ' + completion + '\n'
            
            content3 = {'prompt': promptModified, 'completion': completionModified}
            # print(content3)
            
            cleanedFileName = 'prepared_' + file_path

            with open(cleanedFileName, "a", encoding="UTF-8") as file2:
                json.dump(content3, file2, ensure_ascii=False)
                file2.write('\n')
                
            content1 = file.readline()

def getFileStatus(file_id): #取得已上傳檔案的資訊
    response = openai.File.retrieve(file_id)
    return response

def uploadFile(cleanedFileName): #將準備好的JsonL的檔案交給openai File.create上傳檔案
    
    # 上傳資料
    response = openai.File.create(file=open(cleanedFileName, "rb"), purpose="fine-tune")
    
    # 取得上傳後的資料ID
    file_id = response["id"]
    
    # 取得資料處理進度
    response = openai.File.retrieve(file_id)
    
    return file_id