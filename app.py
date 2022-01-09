
# flask 架設伺服器，沒畫面
# django 架設更大規模的伺服器，有畫面的網址，做網頁的
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('+XETi1eQhfd/XXGX8j2ZZxw8L6hB4vtUZHLNE7xh/oyQiXMQmhFHkvWTb4IBdHVt5ZHOdFigBgk7+gXj9NgcxgNpSiih6y/mn0kt+7AwoNT1XkZzUFNZr1Gb+mNIngGdmSab9nRu8RU9oZP1XnAUbQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('22f21690a2d119a9d8d0c9f3e4f1b2d9')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()