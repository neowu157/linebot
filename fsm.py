from transitions.extensions import GraphMachine
from utils import send_text_message, send_carousel_message, send_button_message, send_image_message
from linebot.models import ImageCarouselColumn, URITemplateAction, MessageTemplateAction

# global variable
gender = ''
height = 0
weight = 0

class TocMachine(GraphMachine):

    def __init__(self, **machine_configs):
        self.machine = GraphMachine(model=self, **machine_configs)

    # user start
    def is_going_to_input_gender(self, event):
        text = event.message.text
        return text.lower() == 'bmi'

    def on_enter_input_gender(self, event):
        title = '請先提供您的基本資訊'
        text = '您是『男生』還是『女生』'
        btn = [
            MessageTemplateAction(
                label = '男生',
                text ='男生'
            ),
            MessageTemplateAction(
                label = '女生',
                text = '女生'
            ),
        ]
        url = 'https://i.imgur.com/T2bLdbN.jpg'
        send_button_message(event.reply_token, title, text, btn, url)


    def is_going_to_input_height(self, event):
        global gender
        text = event.message.text

        if text == '男生':
            gender = '男生'
            return True
        elif text == '女生':
            gender = '女生'
            return True
        return False

    def on_enter_input_height(self, event):
        send_text_message(event.reply_token, '請輸入您的身高(整數)')

    def is_going_to_input_weight(self, event):
        global height
        text = event.message.text

        if text.lower().isnumeric():
            height = int(text)
            return True
        return False

    def on_enter_input_weight(self, event):
        send_text_message(event.reply_token, '請輸入您的體重(整數)')

    def is_going_to_show_result(self, event):
        global weight
        text = event.message.text

        if text.lower().isnumeric():
            weight = int(text)
            return True
        return False

    def on_enter_show_result(self, event):
        global gender,height,weight
        x=weight/((height/100)*(height/100))
        if gender=='男生':
            if x<=31 and x>=17:
                result ='常備役'
            elif x>31 and x<=31.5:
                result ='替代役'
            elif x<17 and x>=16.5:
                result ='替代役'
            elif x<16.5:
                result ='免役'
            elif x>31.5:
                result ='免役'
        elif gender=='女生':
            result='不用當兵'

        result=result+',你的bmi為:'+str(round(x,1))
        send_text_message(event.reply_token, result)



