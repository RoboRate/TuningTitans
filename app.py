import os
from flask import Flask, redirect, render_template, request, session, url_for, send_file,g
import openai
import pymysql
import shutil
import json
import tempfile
from models import createJsonlFromDocuments
import finetuneModelCreate as createModel
import finetunePrepareData as prepareData
import Benchmark as benchmarkreport
from werkzeug.utils import secure_filename
import tempfile
import atexit
import shutil
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

@app.route("/qadesign", methods=["GET", "POST"])
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
                #previewData = content  # 將檔案內容傳遞到前端供預覽
                
                # Create an uploads_directory to store the uploaded files
                uploads_directory = './uploads'
                os.makedirs(uploads_directory, exist_ok=True)
                
                # 儲存上傳的檔案至伺服器端，以便下載
                temp_dir = tempfile.mkdtemp(dir=uploads_directory)
                filePath = os.path.join(temp_dir, filename)
                
                with open(filePath, 'w', encoding='utf-8') as file:
                    file.write(content)  # 將內容寫入文件
                    
                
                    # Generate the JSONL data from the uploaded documents轉檔JSONL神器
                result = createJsonlFromDocuments(temp_dir)  # 提供目錄路徑
                output_file = os.path.join(uploads_directory, 'output.jsonl')
                    
                with open(output_file, 'w', encoding='utf-8') as file:
                    for item in result:
                        file.write(json.dumps(item, ensure_ascii=False) + '\n')
                    #return send_file(output_file, as_attachment=True)
                previewData = result
                atexit.register(cleanup)
    return render_template("index.html", previewData=previewData, filePath=filePath)
uploads=None
def cleanup():
    if uploads:
        try:
            shutil.rmtree(uploads)  # 直接刪除整個文件夾及其內容
        except Exception as e:
            print(f"Error while cleaning up: {e}")


@app.route("/finetuning", methods=["GET", "POST"])
def finetuning():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    status = None
    
    if request.method == "POST":
        # 獲取上傳的檔案
        training_file = request.files["training_file"]
        validation_file = request.files["validation_file"]
        
        if training_file and validation_file:
            # 保存上傳檔案
            training_file_path = os.path.join("uploads", "training.jsonl")
            validation_file_path = os.path.join("uploads", "validation.jsonl")
            training_file.save(training_file_path)
            validation_file.save(validation_file_path)
            
            # 處理檔案成符合 openai 要求的格式
            prepareData.fileTransferToPreparedData(training_file_path)
            prepareData.fileTransferToPreparedData(validation_file_path)
            
            # 上傳檔案並獲取檔案資訊
            training_file_id = prepareData.uploadFile(training_file_path)
            validation_file_id = prepareData.uploadFile(validation_file_path)
            
            training_file_status = prepareData.getFileStatus(training_file_id)
            validation_file_status = prepareData.getFileStatus(validation_file_id)
            
            status = {
                "training_file_id": training_file_id,
                "training_file_status": training_file_status,
                "validation_file_id": validation_file_id,
                "validation_file_status": validation_file_status
            }
            
    return render_template("api2.html", status=status)

@app.route("/train_model", methods=["POST"])
def train_model():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    training_file = request.form.get("training_file")
    validation_file = request.form.get("validation_file")
    model = request.form.get("model")
    n_epochs = request.form.get("n_epochs")
    batch_size = request.form.get("batch_size")
    learning_rate_multiplier = request.form.get("learning_rate_multiplier")
    
    # 呼叫 modelCreate 函式進行模型訓練
    model_info = createModel.modelCreate(
        training_file=training_file,
        validation_file=validation_file,
        model=model,
        n_epochs=n_epochs,
        batch_size=batch_size,
        learning_rate_multiplier=learning_rate_multiplier
    )
    
    model_status = {
        "fine_tuned_model": model_info["fine_tuned_model"],
        "model_id": model_info["id"],
        "status": model_info["status"]
    }
    
    return render_template("api2.html", status=None, model_status=model_status)


@app.route("/get_model_status", methods=["GET"])
def get_model_status():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    model_id = request.args.get("model_id")
    
    if model_id:
        # 呼叫 modelStatusCheck 函式取得模型訓練狀態
        model_status = createModel.modelStatusCheck(model_id)
        
    return render_template("api2.html", model_status=model_status)


@app.route("/get_model_result/<model_result_file_id>")
def get_model_result(model_result_file_id):
    # 根據 model_result_file_id 取得模型結果
    model_result = createModel.getModelAnalysis(model_result_file_id)
    
    # 確保 temp 資料夾存在
    temp_folder = "./ModelAnalysis"
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    
    # 將 CSV 內容寫入暫時的檔案
    temp_file_path = os.path.join(temp_folder, model_result_file_id + "_modelAnalysis.csv")
    with open(temp_file_path, "w", encoding="UTF-8") as file:
        file.write(model_result)
    
    # 使用 send_file 下載暫時的檔案並保持在頁面上
    return send_file(temp_file_path, as_attachment=True, attachment_filename="modelAnalysis.csv")

@app.route("/benchmark", methods=["GET", "POST"])
def benchmark():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    
    results = []
    
    if request.method == "POST":
        # 獲取上傳的檔案
        qna_data = request.files["qna_data"]
        fine_tuned_model_id = request.form.get("fine_tuned_model_id")
        #從fine_tuned_model_id提取出raw_model的名稱
        raw_model = fine_tuned_model_id.split(":")[0]
        model_names = [fine_tuned_model_id, raw_model]

        if qna_data and fine_tuned_model_id and model_names:
            #暫時儲存上傳檔案
            temp_file_path = os.path.join(tempfile.gettempdir(), secure_filename(qna_data.filename))
            qna_data.save(temp_file_path)
            # 呼叫generateAnswers函式取得模型問答結果
            for model_name in model_names:
                model_result = benchmarkreport.generateAnswers(dataset_path=temp_file_path, model_name=model_name)
                model_evaluation = benchmarkreport.evalWithRubric(model_result)

                results.append({
                    "model_name": model_name,
                    "model_result": model_result,
                    "model_evaluation": model_evaluation
                })
            os.remove(temp_file_path)
    return render_template("api3.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
