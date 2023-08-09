import os
from flask import Flask, redirect, render_template, request, session, url_for, send_file
import openai
import pymysql
import shutil
import json
from models import createJsonlFromDocuments
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
userAccount = os.getenv("USER_ACCOUNT")
userPassword = os.getenv("USER_PASSWORD")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        # 身分驗證
        if name == userAccount and password == userPassword:
            session["logged_in"] = True
            return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    previewData = None  # 初始化檔案預覽內容為空
    filePath = None  # 初始化檔案路徑為空

    # 現在可以在這裡處理表單提交，因為使用者已經登入
    if request.method == "POST":
        files = request.files["fileToUpload"]
        if files:
            filename = files.filename
            if filename.endswith(".txt") or filename.endswith(".csv"):
                content = files.read().decode("utf-8")
                previewData = content  # 將檔案內容傳遞到前端供預覽
                # Create a uploads_directory to store the uploaded files
                uploads_directory = './uploads'
                os.makedirs(uploads_directory, exist_ok=True)
                # 儲存上傳的檔案至伺服器端，以便下載
                filePath = os.path.join("uploads", filename)
                files.save(filePath)
                try:
                # Generate the JSONL data from the uploaded documents轉檔JSONL神器
                    result = createJsonlFromDocuments(filePath)
                # Write the JSONL data to the output file
                    output_file = './uploads/output.jsonl'  # 暫存
                    with open(output_file, 'w', encoding='utf-8') as file:
                        for item in result:
                            file.write(json.dumps(item, ensure_ascii=False) + '\n')
                    return send_file(output_file, as_attachment=True)
                finally:
                # Remove the uploads_directory after processing
                    shutil.rmtree(uploads_directory)
    return render_template("index.html", previewData=previewData, filePath=filePath)
    
if __name__ == "__main__":
    app.run(debug=True)
