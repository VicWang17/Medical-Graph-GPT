from flask import Flask
from api import beimin
app=Flask(__name__)
app.register_blueprint(beimin,url_prefix="/chat")
if __name__=="__main__":
    app.run(host="0.0.0.0",port=3006)

