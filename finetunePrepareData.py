import openai
import os

openai.organization = os.getenv("OPENAI_API_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")

file_id = os.getenv("OPENAI_FILE_ID")
file_path = "cleaned.jsonl"


def getFileStatus(file_id): #取得上傳檔案的狀態，是否已驗證完成
    response = openai.File.retrieve(file_id)
    return response


def validateJsonlFile(file_path): #將JsonL的檔案交給openai提供的工具File.create與File.retrieve做資料驗證
    
    # 上傳資料
    response = openai.File.create(file=open(file_path, "rb"), purpose="fine-tune")
    
    # 取得上傳後的資料ID
    file_id = response["id"]
    print(file_id)
    
    # 取得資料處理進度
    response = openai.File.retrieve(file_id)
    print(response["status"])
    
    # 取得已驗證的資料內容
    # response = openai.File.retrieve(file_id)
    # print(response["file"]["filename"])
    # print(response["file"]["url"])
    
    return file_id



if __name__ == "__main__":
    response = getFileStatus(file_id)
    print(response)