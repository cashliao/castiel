import formosa as fa
import pandas as pd
from flask import Flask, request, abort
from linebot import ( LineBotApi, WebhookHandler )
from linebot.exceptions import ( InvalidSignatureError )
from linebot.models import ( MessageEvent, TextMessage, TextSendMessage,)

app = Flask(__name__)
line_bot_api = LineBotApi('G9OB17MVZ9MECtlpwkr1XLRdxBP37r9b+ED3TmDaE9lDzUso2ksjmWmRtmCmkVWa2vAh63vbglEQb69dFXHDSyqPxUBV7/zqf6lIQb3Yad/Rg2v8pg97U609d0p9NDeRZ5rgpDFamVcWAYJfg/9q4gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('94742205abcd0a58016c02d658cfb6e5')

@app.route("/callback", methods=['POST'])

def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    if event.message.text=='人數':
        fa.download_new_csv()
        fa.download_old_csv()
        new_members = fa.resolve_new_members(fa.load_new_csv())
        old_members = fa.resolve_old_members(fa.load_old_csv())
        all_members = fa.get_all_members(new_members,old_members)
        summary_report = fa.get_summary_report(all_members)
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=summary_report))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=443,debug = True, ssl_context=('/home/src/server.crt', '/home/src/server.key'))
    #app.run(host='0.0.0.0',port=80,debug=True)
    res.end('hello');

