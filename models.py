
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import DirectoryLoader
import json

def create_jsonl_from_documents(directory_path):
    loader = DirectoryLoader(directory_path, glob='**/*.txt') #glob='**/*.txt'表示讀取所有子目錄下的所有txt文件
    documents = loader.load()
# chunk_size表示每個文本塊的大小為 100 個字符。也就是說，原始文本將被切割成長度為 100 的多個小塊，假設原始文本長度為 1000，那麼將被切割成 10 個文本塊
# chunk_overlap表示每個文本塊的重疊大小為 0 個字符。也就是說，每個文本塊之間沒有重疊
    text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    split_docs = text_splitter.split_documents(documents)

    result = []

    for i in range(len(split_docs) - 1):
        prompt_text = split_docs[i].page_content # prompt_text是前一個文本塊的內容
        ideal_generated_text = split_docs[i + 1].page_content # ideal_generated_text是後一個文本塊的內容
        result.append({"prompt": prompt_text, "completion": ideal_generated_text})

    return result
##############################################
#function本地端測試
# if __name__ == "__main__":
#     directory_path = r'C:\Users\USER\Desktop\小鎮智能\訓練集\smile'
#     result = create_jsonl_from_documents(directory_path)
# # 將結果寫入 JSONL 文件
#     with open('output.jsonl', 'w', encoding='utf-8') as file:
#         for item in result:
#             # 確保寫入時使用 UTF-8 編碼，並處理非 ASCII 字符
#             file.write(json.dumps(item, ensure_ascii=False) + '\n')
#function本地端測試

