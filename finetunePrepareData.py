import openai
import os
import json

# openai.organization = os.getenv("OPENAI_API_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

file_id = os.getenv("OPENAI_TRAININGFILE_ID")
file_path = os.getenv("SOURCE_FILE")
cleanedFileName = os.getenv("PREPARED_FILE")

def fileTransferToPreparedData(): #將原始Jsonl檔案，按照openai訓練模型要求，prompt的suffix加上" ->"，completion的suffix加上 "\n"
    with open (file_path, "r", encoding="UTF-8") as file:
        content1 = file.readline()
        while content1:
            content2 = json.loads(content1.strip())
            
            prompt = content2['prompt']
            completion = content2['completion']
            
            promptModified = prompt + ' ->'
            completionModified = completion + '\n'
            
            content3 = {'prompt': promptModified, 'completion': completionModified}
            # print(content3)

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
    print(file_id)
    
    # 取得資料處理進度
    response = openai.File.retrieve(file_id)
    print(response["status"])
    
    return file_id


if __name__ == "__main__":
    response = getFileStatus(file_id)
    print(response)