
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

line_bot_api = LineBotApi('1B7uGW0uAZ4CN3jlmtZLjnEYEsN6WmzgHTQ8OD6582iVhAtG+8enjlzNw27oZyjF5ZHOdFigBgk7+gXj9NgcxgNpSiih6y/mn0kt+7AwoNSrJ+G7lucSWupv/uN3LzRh8hHio+QRvWCuWLjWyE4A/AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5834f7f2dff8238b8878c9dd5083fe73')


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