import os
from flask import Flask, redirect, render_template, request, session, url_for, send_file
import openai
import pymysql

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
        file = request.files["fileToUpload"]
        if file:
            filename = file.filename
            if filename.endswith(".txt") or filename.endswith(".csv"):
                content = file.read().decode("utf-8")
                previewData = content  # 將檔案內容傳遞到前端供預覽

                # 儲存上傳的檔案至伺服器端，以便下載
                filePath = os.path.join("uploads", filename)
                file.save(filePath)

                # 儲存內容至檔案
                with open(os.path.join("uploads", filename), "w", encoding="utf-8",newline=os.linesep) as f:
                    f.write(content)

    return render_template("index.html", previewData=previewData, filePath=filePath)

if __name__ == "__main__":
    app.run(debug=True)
