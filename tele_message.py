from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import threading

class Telegrams():

    def __init__(self):

        self.sell_temp_gubun = None
        self.tr_temp = None

        self.updater = Updater("tele api", use_context=True)
        message_handler = MessageHandler(Filters.text & (~Filters.command), self.get_message)
        self.updater.dispatcher.add_handler(message_handler)

        #----------------메세지 보내는 명령어--------------
        # self.updater.bot.send_message(chat_id="1505160195", text="텔레그램 활성화")
        #----------------------------------------------

        threading.Thread(target=self.check_msg, args=(self.updater,), daemon= True).start()

        #-----여기서부터는 텔레그램에서 사용할 명령어를 다루는 것------

        help_handler = CommandHandler('help', self.help_command)   #텔레그램에서 /help치면 self.help_command 함수가 실행이 됨
        self.updater.dispatcher.add_handler(help_handler)  #핸들러를 추가해줌

        #-------------------------------------------
        help_handler = CommandHandler('stocks_sell', self.sell_command) # 종목매도_sell 한글 안 돼서 변경
        self.updater.dispatcher.add_handler(help_handler)

        help_handler = CommandHandler('yes', self.yes_command) ##yes와 no에 각각 매수시, 매도시 명령어 로직을 작성해놔야함
        self.updater.dispatcher.add_handler(help_handler)
        help_handler = CommandHandler('no', self.no_command)
        self.updater.dispatcher.add_handler(help_handler)
        #-------------------------------------------

        help_handler = CommandHandler('alarm', self.alarm_command)   #체결시 알람
        self.updater.dispatcher.add_handler(help_handler)


        help_handler = CommandHandler('tr_request', self.tr_command) #tr요청 한글 안 돼서 변경
        self.updater.dispatcher.add_handler(help_handler)

    def get_message(self, update, context):
        print("메세지 수신: %s" %  update.message.text)
        print(context)

    # 쓰레딩으로 동작시킨 함수
    def check_msg(self, up_data):
        # start_polling으로 새로운 메시지가 있는지 체크하고 주기적으로 데이터들을 비워준다.
        up_data.start_polling(timeout=3, poll_interval=2, drop_pending_updates=True)

    # 내가 만든 명령어를 텔레그램에서 작성하면 여기서 수신된다.
    def help_command(self, update, context):
        txt = "/help 도움말\n\n" \
              "/stocks_sell\n\n" \
              "/tr요청\n\n"

        update.message.reply_text(txt)      #프로그램 => 텔레그램으로 송신

    def sell_command(self, update, context):
        self.sell_temp_gubun = "종목매도"
        update.message.reply_text("한 번 실행하면 되돌릴 수 없습니다. 실행하시겠습니까?\n/yes          /no")

    def yes_command(self, update, context):
        if self.sell_temp_gubun is not None:
            print("종목을 매도하는 로직을 추가")
            update.message.reply_text("종목을 매도하는 로직을 추가")
        self.sell_temp_gubun = None

    def no_command(self, update, context):
        self.sell_temp_gubun = None

    def tr_command(self, update, context):
        self.tr_temp = "tr이름"
        threading.Timer(5.1, self.tr_req_chk).start()

    def tr_req_chk(self, update):
        self.tr_temp = None

    def alarm_command(self, text):
        if text == "a":
            self.updater.bot.send_message(chat_id="1505160195", text="체결완료 : 업비트 매수 + 빗썸 매도")
        elif text == "b":
            self.updater.bot.send_message(chat_id="1505160195", text="체결완료 : 빗썸 매수 + 업비트 매도")
        elif text == "c":
            self.sell_temp_gubun = "종목매도"
            self.updater.bot.send_message(chat_id="1505160195", text="upbit 일부 미체결되어 중지됨")

            # update.message.reply_text("쓰레드를 다시 실행하시겠습니까?\n/yes          /no")

        elif text == "d":
            self.sell_temp_gubun = "종목매도"
            self.updater.bot.send_message(chat_id="1505160195", text="bithumb 일부 미체결되어 중지됨")

        elif text == "e":
            self.updater.bot.send_message(chat_id="1505160195", text="bithumbSellBuyError 오류로 중지됨")

            # update.message.reply_text("쓰레드를 다시 실행하시겠습니까?\n/yes          /no")
