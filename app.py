from flask import Flask
from datetime import datetime

app = Flask(__name__)
@app.route("/")
def helloworld():
    timenow = datetime.now()
    date_time = timenow.strftime("%m/%d/%Y, %H:%M:%S")
    return f"Hello World from Yan! {date_time}"
if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)
