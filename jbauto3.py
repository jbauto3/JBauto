import time, datetime, pybithumb, pyupbit, math
import tele_message
import threading

class TradeCurrencyWorker():

    def __init__(self, ticker, ticker2):
        self.ticker = ticker
        self.ticker2 = ticker2
        self.alive = True
        self.tele = tele_message.Telegrams()

        Bit_apikey = 
        Bit_seckey = 
        Upb_apikey =
        Upb_seckey =

        self.bithumb = pybithumb.Bithumb(Bit_apikey, Bit_seckey)
        self.upbit = pyupbit.Upbit(Upb_apikey, Upb_seckey)


        print("-------START--------")
        bithumbAvailableKRW = self.bithumb.get_balance(self.ticker)[2]
        upbitAvailableKRW = int(self.upbit.get_balance("KRW"))
        bit_bal = math.trunc(bithumbAvailableKRW)
        bit_bal2 = format(bit_bal, ',')
        upb_bal = format(upbitAvailableKRW, ',')
        print("Bithumb KRW : {} Won".format(bit_bal2))
        print("Upbit KRW : {} Won".format(upb_bal))

    def close(self):
        self.alive = False

    def run(self):

        while self.alive:
            try:
                bithumbOrderbook = pybithumb.get_orderbook(self.ticker, limit=10)
                bit_bid = bithumbOrderbook["bids"][0]["price"]
                bit_ask = bithumbOrderbook["asks"][0]["price"]

                if bit_bid < 1000:
                    pass
                else:
                    bit_bid = int(bit_bid)

                if bit_ask < 1000:
                    pass
                else:
                    bit_ask = int(bit_ask)
                #---------------------------------------------------

                bit_bid_qty = round(float(bithumbOrderbook["bids"][0]["quantity"]),3)  
                bit_ask_qty = round(float(bithumbOrderbook["asks"][0]["quantity"]),3) 

                upbitOrderbook = pyupbit.get_orderbook(self.ticker2)
                
                BTC_price = pyupbit.get_current_price("KRW-BTC")


                upb_bid = float(upbitOrderbook["orderbook_units"][0]["bid_price"])
                upb_ask = float(upbitOrderbook["orderbook_units"][0]["ask_price"])
                upb_bid_qty = round(float(upbitOrderbook["orderbook_units"][0]["bid_size"]),3)
                upb_ask_qty = round(float(upbitOrderbook["orderbook_units"][0]["ask_size"]),3)
                bithumbBalnace = self.bithumb.get_balance(self.ticker)
                bithumbAvailableKRW = bithumbBalnace[2]
                bithumbAvailableCur = bithumbBalnace[0]
                upbitAvailableKRW = int(self.upbit.get_balance("KRW"))
                upbitAvailableCur = float(self.upbit.get_balance(self.ticker2))
                upbitAvailableBTC = self.upbit.get_balance("BTC")

                data = [bit_bid, bit_bid_qty, bit_ask, bit_ask_qty, upb_bid, upb_bid_qty, upb_ask, upb_ask_qty,
                        bithumbAvailableKRW, bithumbAvailableCur, upbitAvailableKRW, upbitAvailableCur, upbitAvailableBTC, BTC_price]

                if data != None and self.alive == True:
                    now = datetime.datetime.now()
                    formatDate = now.strftime("[%H:%M:%S]")
                    KRW_upb_bid = upb_bid * BTC_price
                    KRW_upb_ask = upb_ask * BTC_price

              
                    if bit_bid - KRW_upb_ask >= KRW_upb_ask * margin:
                        perc = (bit_bid / KRW_upb_ask) - 1

                        market_bid = bit_bid  #
                        market_ask = KRW_upb_ask  #

                
                        if upb_ask_qty < qty or bit_bid_qty < qty:
                            print(formatDate + "Lack of quantity")
                            return trade.run()
                        if upbitAvailableBTC < upb_ask * qty:
                            print(formatDate + "Lack of upbit BTC")
                            return trade.run()
                        if round(bithumbAvailableCur, 4) < qty:
                            print(formatDate + "Lack of bithumb currency")
                            return trade.run()
                        # --------------------------------------------

                        if upbitAvailableBTC > upb_ask * qty and bithumbAvailableCur > qty:
                            print("Trade Start == upbit buy + bithumb sell")
                            print("Price Differ : {}%".format(round(perc, 4) * 100))
                            print(formatDate + "   Upbit {}won buy + bithumb {}won sell".format(math.trunc(KRW_upb_ask), bit_bid))
                            bithumbSellBuyError = self.bithumb.sell_limit_order(self.ticker, market_bid, qty)  #

                            if bithumbSellBuyError['status'] == '0000':
                                order_desc1 = ('ask', self.ticker, bithumbSellBuyError['order_id'], "KRW")
                                after_bitAvailableCur = self.bithumb.get_balance(self.ticker)[0]
                                after_bitAvailableKRW = self.bithumb.get_balance(self.ticker)[2]
                                outstanding2 = self.bithumb.get_outstanding_order(order_desc1)

                                if math.isclose(bithumbAvailableCur - qty, after_bitAvailableCur) \
                                        or bithumbAvailableKRW < after_bitAvailableKRW or outstanding2 == None:

                                    # TODO 확인용
                                    print(formatDate, bithumbAvailableCur, after_bitAvailableCur, bithumbAvailableKRW,
                                          after_bitAvailableKRW,
                                          outstanding2, bit_ask, bit_ask_qty)

                                    pass
                                elif math.isclose(bithumbAvailableCur, after_bitAvailableCur) or \
                                        after_bitAvailableKRW == bithumbAvailableKRW or math.isclose(float(outstanding2), qty):
                                    self.bithumb.cancel_order(order_desc1)

                                    # TODO 확인용
                                    print(formatDate, bithumbAvailableCur, after_bitAvailableCur, bithumbAvailableKRW,
                                          after_bitAvailableKRW,
                                          outstanding2, bit_ask, bit_ask_qty)

                                    print("Order cancel : Bithumb contract failure ")
                                    get_trade.close()
                                    time.sleep(2)
                                    self.alive = True
                                    return trade.run()
                                else: 
                                    print("Order cancel : Bithumb some contracts failure ")
                                    get_trade.close()
                                    print("-------Thread stop--------")
                                    self.tele.alarm_command("d")
                                    return False

                            elif bithumbSellBuyError['status'] != '0000':
                                print("bithumbSellBuyError Error")
                                print("Error Code : {}".format(bithumbSellBuyError))
                                get_trade.close()
                                print("-------Thread stop--------")
                                self.tele.alarm_command("e")
                                return False

                            upbSellBuyError = self.upbit.buy_limit_order(self.ticker2, upb_ask, qty)
                            after_upbitAvailableCur = float(self.upbit.get_balance(self.ticker2))
                            after_upbBTC_bal = self.upbit.get_balance("BTC")

                            if type(upbSellBuyError) == dict:
                                if math.isclose(upbitAvailableCur + qty, after_upbitAvailableCur) or \
                                        upbitAvailableBTC != after_upbBTC_bal or \
                                        self.upbit.get_order(upbSellBuyError['uuid'])['state'] == "done":

                                    try:
                                        BTC_buy = self.upbit.buy_market_order("KRW-BTC", qty * market_ask)
                                        if BTC_buy == None:
                                            print("Not available to purchase - Lack of KRW balance")
                                            print("Error Code - {}".format(BTC_buy))
                                            print("-------Thread stop--------")
                                            get_trade.close()
                                            return False
                                    except:
                                        print("BTC purchase failure : don't know err")
                                        print("-------Thread stop--------")
                                        get_trade.close()
                                else:
                                    print("Upbit some contracts failure")
                                    get_trade.close()
                                    self.tele.alarm_command("c")
                                    return False

                            elif type(upbSellBuyError) != dict:
                                print("upbSellBuyError Err = contract failure")
                                print("Error code : {}".format(upbSellBuyError))
                                self.bithumb.buy_limit_order(self.ticker, market_bid,qty)
                                print("-------Thread stop--------")
                                get_trade.close()
                                return False

                            print("Trade Complete")
                            self.tele.alarm_command("a")

                    #TODO bithumb buy/upbit sell
                    elif KRW_upb_bid - bit_ask >= bit_ask * margin:  #
                        perc2 = (KRW_upb_bid / bit_ask) - 1
                        market_ask = bit_ask  #

                        if upb_bid_qty < qty or bit_ask_qty < qty:  #
                            print(formatDate + "Lack of market quantity")
                            return trade.run()
                        if bithumbAvailableKRW < market_ask * qty:
                            print(formatDate + "Lack of Bithumb KRW bal")
                            return trade.run()

                        after_upbitAvailableCur = float(self.upbit.get_balance(self.ticker2))

                        if round(after_upbitAvailableCur, 4) < qty:
                            print(formatDate + "Lack of Upbit KRW bal")
                            return trade.run()
                        # ---------------------------------------------

                        if bithumbAvailableKRW >= market_ask * qty and after_upbitAvailableCur >= qty:
                            print("Price differ : {}%".format(round(perc2, 4) * 100))
                            print(formatDate + "   bithumb {}won buy + upbit {}won sell".format(bit_ask, math.trunc(KRW_upb_bid)))
                            bithumbSellBuyError = self.bithumb.buy_limit_order(self.ticker, market_ask, qty)

                            if bithumbSellBuyError['status'] == "0000":
                                order_desc2 = ('bid', self.ticker, bithumbSellBuyError['order_id'], 'KRW')
                                after_bitAvailableCur = float(self.bithumb.get_balance(self.ticker)[0])
                                after_bitAvailableKRW = self.bithumb.get_balance(self.ticker)[2]
                                outstanding2 = self.bithumb.get_outstanding_order(order_desc2)

                                if math.isclose(bithumbAvailableCur + qty, after_bitAvailableCur) or \
                                        bithumbAvailableKRW > after_bitAvailableKRW or outstanding2 == None :

                                    # TODO 확인용
                                    print(formatDate, bithumbAvailableCur, after_bitAvailableCur, bithumbAvailableKRW,
                                          after_bitAvailableKRW,
                                          outstanding2, bit_ask, bit_ask_qty)

                                    pass
                                elif math.isclose(bithumbAvailableCur, after_bitAvailableCur) or \
                                        after_bitAvailableKRW == bithumbAvailableKRW or math.isclose(float(outstanding2), qty):


                                    # TODO 확인용
                                    print(formatDate, bithumbAvailableCur, after_bitAvailableCur, bithumbAvailableKRW,
                                          after_bitAvailableKRW,
                                          outstanding2, bit_ask, bit_ask_qty)

                                    self.bithumb.cancel_order(order_desc2)
                                    print("Order cancel : bithumb contract failure ")
                                    get_trade.close()
                                    time.sleep(2)
                                    self.alive = True
                                    return trade.run()
                                else: 
                                    print("Order cancel : bithumb some contracs failure  ")
                                    get_trade.close()
                                    print("-------Thread stop--------")
                                    self.tele.alarm_command("d")
                                    return False
                            elif bithumbSellBuyError['status'] != "0000":
                                print("bithumbSellBuyError Error")
                                print("Error code : {}".format(bithumbSellBuyError))
                                print("-------Thread stop--------")
                                self.tele.alarm_command("e")
                                get_trade.close()
                                return False

                            upbSellBuyError = self.upbit.sell_limit_order(self.ticker2, upb_bid, qty)
                            after_upbitAvailableCur = float(self.upbit.get_balance(self.ticker2))
                            after_upbBTC_bal = self.upbit.get_balance("BTC")
                            if type(upbSellBuyError) == dict:
                                if math.isclose(upbitAvailableCur - qty, after_upbitAvailableCur) or \
                                        upbitAvailableBTC != after_upbBTC_bal or self.upbit.get_order(upbSellBuyError['uuid'])['state'] == "done":
                                    try:
                                        BTC_buy = self.upbit.sell_market_order("KRW-BTC", qty * upb_bid)
                                        if BTC_buy == None:
                                            print("Not available to purchase BTC - Lack of KRW bal")
                                            print("Error code - {}".format(BTC_buy))
                                            print("-------Thread stop--------")
                                            get_trade.close()
                                            return False
                                    except:
                                        print("BTC purchase failure - don't know")
                                        print("-------Thread stop--------")
                                        get_trade.close()
                                        return False
                                else:
                                    print("Upbit doesn't purchased")
                                    get_trade.close()
                                    self.tele.alarm_command("c")
                                    return False
                            elif type(upbSellBuyError) != dict:
                                print("upbSellBuyError Err = contract failure")
                                print("Error code : {}".format(upbSellBuyError))
                                self.bithumb.sell_limit_order(self.ticker, market_ask, qty) 
                                get_trade.close()
                                print("-------Thread stop--------")
                                return False
                            print("Trade done")
                            self.tele.alarm_command("b")

                    else:
                        print(formatDate + "Searching price diff")

                else:
                    print(data)
                    get_trade.close()
                    return trade.run()

            except TypeError:
                print("TradeCurrencyWorker / data upload fail : TypeError")
                return False



if __name__ == "__main__":
    ticker, ticker2 = input("Bithumb ticker , Upbit ticker : ").split(",")
    qty, margin = map(float, input("qty , margin : ").split(","))
    trade = TradeCurrencyWorker(ticker, ticker2)
    get_trade = threading.Thread(target=trade.run)
    get_trade.start()
