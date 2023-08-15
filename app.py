import os
from flask import Flask, redirect, render_template, request, session, url_for
import openai
import pymysql
from tempfile import NamedTemporaryFile


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
UserAccount = os.getenv("USER_ACCOUNT")
UserPassword = os.getenv("USER_PASSWORD")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        # 身分驗證
        if name == UserAccount and password == UserPassword:
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

    if request.method == "POST":
        # 現在可以在這裡處理表單提交，因為使用者已經登入
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)

def generate_prompt(animal):
    return """Suggest three names for an animal that is a superhero.

Animal: Cat
Names: Captain Sharpclaw, Agent Fluffball, The Incredible Feline
Animal: Dog
Names: Ruff the Protector, Wonder Canine, Sir Barks-a-Lot
Animal: {}
Names:""".format(
        animal.capitalize()
    )









#######################Benchmark
# @app.route('/', methods=['GET', 'POST'])
# def BenchmarkReport():
#     if request.method == 'POST':
#         uploaded_file = request.files['jsonl_file']
#         name = request.form['name']

#         with NamedTemporaryFile(delete=False, suffix='.jsonl') as temp_file:
#             temp_path = temp_file.name
#             uploaded_file.save(temp_path)
#         # Generate answers using the provided dataset_path and model_name
#         dataset_path = temp_path
#         model_name = request.form['model_name']
#         result = generateAnswers(dataset_path, [model_name, "davinci"])
#         print(result)
#         # Evaluate the result using the evalWithRubric function
#         evaluation_output = evalWithRubric(result, [model_name, "davinci"])
#         print(evaluation_output)

#         os.remove(temp_path)  # Clean up the temporary file
#         return render_template('index.html', result=result, evaluation_output=evaluation_output, model_name=model_name)
#     return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)