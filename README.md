# OpenAI Benchmark Framework
這個專案是一個 OpenAI fine-tuning 的自動基準平台 (OpenAI benchmark framework)，由自然語言的input，透過訓練過的客製化的AI模型，計算出Benchmark而呈現。

# OpenAI API Quickstart - Python example app

This is an example pet name generator app used in the OpenAI API [quickstart tutorial](https://beta.openai.com/docs/quickstart). It uses the [Flask](https://flask.palletsprojects.com/en/2.0.x/) web framework. Check out the tutorial or follow the instructions below to get set up.

## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory:

   ```bash
   $ cd openai-quickstart-python
   ```

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

7. Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

8. Run the app:

   ```bash
   $ flask run
   ```

You should now be able to access the app at [http://localhost:5000](http://localhost:5000)! For the full context behind this example app, check out the [tutorial](https://beta.openai.com/docs/quickstart).


## Reference
本平台的食品安全示範資料集整理自千言袁杰等人的「食品安全主題數據集(https://www.luge.ai/?ref=ruder.io#/luge/dataDetail?id=71)」，僅將其數據內容用於研究和學習目的。

The Mandarin food safety demonstration dataset on this platform has been compiled from the 'Food Safety Themed Dataset' by Yuan Jie, et al. on Qianyan (https://www.luge.ai/?ref=ruder.io#/luge/dataDetail?id=71). We are using the data content solely for research and educational purposes.