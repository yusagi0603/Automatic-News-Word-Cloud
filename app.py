import logging

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

import word_cloud
import line_config

app = Flask(__name__)

line_bot_api = LineBotApi(line_config.LINE_SETTING.get('TOKEN')) # TOKEN
handler = WebhookHandler(line_config.LINE_SETTING.get('SECRET')) # SECRET

wordcloud = word_cloud.NewsWordCloud()

@app.route("/callback", methods=['POST'])
def callback(): 
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as textb
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

    # recevice info from clinet
    user_id = event.source.user_id
    msg =  event.message.text

    # resp based on different scenario
    logging.info('Message: {}'.format(msg))
    
    if msg == ['政治', '財經', '生活', '國際', '政治', '科技']: # not relife
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='請稍後，為您蒐集{news_cate}中'.format(news_cate=msg))
        )
        wordcloud.generate_cloud(keyword=msg)
        # resp = Bot.get_resp(query=msg).get('answer') # (text, similarity) 

    else: # relife
        resp = '您可透過輸入以下的關鍵字來獲得各類新聞的文字雲\n 「政治」、「財經」、「生活」、「國際」、「政治」、「科技」'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=resp)
        )

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=resp))


if __name__ == "__main__":
    
    app.run(port=8080) # set the same number with parameter for ngrok
