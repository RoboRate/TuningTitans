import subprocess
from dotenv import load_dotenv
import os
import openai
import pandas as pd 
import io


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

#輸入fine_tune_job_id
YOUR_FINE_TUNE_JOB_ID = " "

command = [
    "openai", "api", "fine_tunes.results",
    "-i", YOUR_FINE_TUNE_JOB_ID
]

results = subprocess.run(command, capture_output=True, text=True)

#得到執行命令後的結果(csv形式)
output = results.stdout

#讀取結果並將結果存成檔案
showresults = pd.read_csv(io.StringIO(output))

showresults.to_csv("fine_tune_results.csv", index=False)

print(showresults)