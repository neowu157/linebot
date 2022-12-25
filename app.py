import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message, send_text_message_AI


load_dotenv()


machine = TocMachine(
    states=[
        'input_gender',
        'input_height',
        'input_weight',
        'show_result'
    ],
    transitions=[
        {'trigger': 'advance', 'source': 'user', 'dest': 'input_gender', 'conditions': 'is_going_to_input_gender'},
        {'trigger': 'advance', 'source': 'input_gender', 'dest': 'input_height', 'conditions': 'is_going_to_input_height'},
        {'trigger': 'advance', 'source': 'input_height', 'dest': 'input_weight', 'conditions': 'is_going_to_input_weight'},
        {'trigger': 'advance', 'source': 'input_weight', 'dest': 'show_result', 'conditions': 'is_going_to_show_result'},
        {
            'trigger': 'go_back',
            'source': [
                'input_gender',
                'input_height',
                'input_weight',
                'show_result'
            ],
            'dest': 'user'
        },
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path='')


channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

@app.route('/callback', methods=['POST'])
def webhook_handler():
    global mode
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f'\nFSM STATE: {machine.state}')
        print(f'REQUEST BODY: \n{body}')



        if event.message.text.lower() == 'fsm':
            send_image_message(event.reply_token, 'https://i.imgur.com/t8CxmXp.png')
        elif machine.state != 'user' and event.message.text.lower() == 'restart':
            send_text_message(event.reply_token, '輸入 bmi 即可開始使用兵役bmi體位小幫手。\n隨時輸入『restart』可以從頭開始。\n隨時輸入『fsm』可以得到當下的狀態圖。')
            machine.go_back()
        else:
            response = machine.advance(event)
            if response == False:
                if machine.state == 'user':
                    send_text_message(event.reply_token,
                                      '輸入 bmi 即可開始使用兵役bmi體位小幫手。\n隨時輸入『restart』可以從頭開始。\n隨時輸入『fsm』可以得到當下的狀態圖。')
                elif machine.state == 'input_height' or machine.state == 'input_weight':
                    send_text_message(event.reply_token, '請輸入一個整數')
                elif machine.state == 'input_gender':
                    send_text_message(event.reply_token, '請輸入『男生』或『女生』')
                elif (machine.state == 'show_result') and (event.message.text.lower() != 'back'):
                    send_text_message(event.reply_token, '輸入『back』返回選單。')


    return 'OK'




def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return send_file('fsm.png', mimetype='image/png')


if __name__ == '__main__':
    port = os.environ.get('PORT', 8000)
    app.run(host='0.0.0.0', port=port, debug=True)
