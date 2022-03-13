import time, datetime, pybithumb, pyupbit, math

class TradeCurrencyWorker():
    def __init__(self, ticker, ticker2):
        self.ticker = ticker
        self.ticker2 = ticker2
        self.alive = True



            Bit_apikey = "access_key"
            Bit_seckey = "sec_key
            Upb_apikey = "access_key"
            Upb_seckey = "sec_key"

            self.bithumb = pybithumb.Bithumb(Bit_apikey, Bit_seckey)
            self.upbit = pyupbit.Upbit(Upb_apikey, Upb_seckey)


        print("-------START--------")
        bithumbAvailableKRW = self.bithumb.get_balance(self.ticker)[2]
        upbitAvailableKRW = int(self.upbit.get_balance("KRW"))
        bit_bal = math.trunc(bithumbAvailableKRW)
        bit_bal2 = format(bit_bal, ',')
        upb_bal = format(upbitAvailableKRW, ',')
        print("빗썸보유현금 : {} 원".format(bit_bal2))
        print("업비트보유현금 : {} 원".format(upb_bal))

    def run(self):                              #"매매시작" 버튼 누르면 얘 돌아감

        while self.alive:
            try:
                #bit 오더북,가격데이터
                bithumbOrderbook = pybithumb.get_orderbook(self.ticker, limit=10)
                bit_bid = bithumbOrderbook["bids"][0]["price"]  # 최상위 매수가격
                bit_ask = bithumbOrderbook["asks"][0]["price"] # 최하위 매도가격

                #빗썸 가격에서 천단위 이상에 소수점 붙으면 limit_order가 안되는 오류때문에 1000원 이상일때 정수로 바꿔줌----
                if bit_bid < 1000:
                    pass
                else:
                    bit_bid = int(bit_bid)

                if bit_ask < 1000:
                    pass
                else:
                    bit_ask = int(bit_ask)
                #---------------------------------------------------

                bit_bid_qty = round(float(bithumbOrderbook["bids"][0]["quantity"]),3)  # 최상위 매수가격 수량
                bit_ask_qty = round(float(bithumbOrderbook["asks"][0]["quantity"]),3)  # 최하위 매도가격 수량

                #upb 오더북,가격 데이터
                upbitOrderbook = pyupbit.get_orderbook(self.ticker2)

                #BTC거래 관련 추가
                BTC_price = pyupbit.get_current_price("KRW-BTC")

                #upb, bit 잔고 데이터
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

                if data != None and self.alive == True: #data가 정상조회될 때,
                    now = datetime.datetime.now()
                    formatDate = now.strftime("[%H:%M:%S]")
                    KRW_upb_bid = upb_bid * BTC_price
                    KRW_upb_ask = upb_ask * BTC_price

                    #TODO-------------bithumb 매도/upbit 매수--------------
                    if bit_bid - KRW_upb_ask >= KRW_upb_ask * margin:
                        perc = (bit_bid / KRW_upb_ask) - 1

                        market_bid = bit_bid  #
                        market_ask = KRW_upb_ask  #

                        # -----------------예외상황--------------------
                        if upb_ask_qty < qty or bit_bid_qty < qty:
                            print(formatDate + "수량부족")
                            return False
                        # BTC 거래 관련 추가
                        if upbitAvailableBTC < upb_ask * qty:
                            print(formatDate + "업비트 BTC 부족")
                            return False
                        if round(bithumbAvailableCur, 4) < qty:
                            print(formatDate + "빗썸 현물부족")
                            return False
                        # --------------------------------------------

                        # BTC 거래 관련 추가
                        if upbitAvailableBTC > upb_ask * qty and bithumbAvailableCur > qty:  # 조건 괜찮으면 빗썸에서 매도+업빗에서 매수 진행
                            print("거래시작 == upbit 매수 + bithumb 매도")
                            print("가격차이비율 : {}%".format(round(perc, 4) * 100))
                            print(formatDate + "   업비트 {}원 구매 + 빗썸 {}원 판매".format(math.trunc(KRW_upb_ask), bit_bid))
                            bithumbSellBuyError = self.bithumb.sell_limit_order(self.ticker, market_bid, qty)  #

                            # -----------------체결 성공시 미체결조회주문------------------
                            if bithumbSellBuyError['status'] == '0000':
                                order_desc1 = ('ask', self.ticker, bithumbSellBuyError['order_id'], "KRW")
                                after_bitAvailableCur = self.bithumb.get_balance(self.ticker)[0]
                                after_bitAvailableKRW = self.bithumb.get_balance(self.ticker)[2]

                                if math.isclose(bithumbAvailableCur - qty, after_bitAvailableCur) \
                                        or bithumbAvailableKRW < after_bitAvailableKRW:  # 거래 정상 진행시
                                    pass
                                elif math.isclose(bithumbAvailableCur, after_bitAvailableCur) or \
                                        after_bitAvailableKRW == bithumbAvailableKRW:  # 전량 미체결 시 (기존pci잔고,잔액 = 거래후 pci 잔고,잔액)
                                    self.bithumb.cancel_order(order_desc1)  # 주문취소
                                    print("주문 취소 : {사유} = 빗썸체결실패 ")
                                    #TODO 스레드 멈춘 후 다시 run 돌리면 정상작동되는지 불확실
                                    get_trade.close()
                                    time.sleep(2)
                                    self.alive = True
                                    return False
                                else:  # 일부 미체결시
                                    print("주문 취소 : {사유} = 빗썸일부미체결 ")
                                    get_trade.close()
                                    print("-------쓰레드중지--------")
                                    self.tele.alarm_command("d")
                                    return False

                            # ------------------매도 실패시------------------
                            elif bithumbSellBuyError['status'] != '0000':
                                print("bithumbSellBuyError 오류")
                                print("오류내용 : {}".format(bithumbSellBuyError))
                                get_trade.close()
                                print("-------쓰레드중지--------")
                                self.tele.alarm_command("e")
                                return False

                            upbSellBuyError = self.upbit.buy_limit_order(self.ticker2, upb_ask, qty)
                            after_upbitAvailableCur = float(self.upbit.get_balance(self.ticker2))
                            after_upbBTC_bal = self.upbit.get_balance("BTC")

                            if type(upbSellBuyError) == dict:  # 거래가 정상적으로 진행되고,
                                # 코인 수 변화있거나, BTC잔액 변화있거나, 주문상태가 done이라면 == 정상주문 진행되었다면,
                                if math.isclose(upbitAvailableCur + qty, after_upbitAvailableCur) or \
                                        upbitAvailableBTC != after_upbBTC_bal or \
                                        self.upbit.get_order(upbSellBuyError['uuid'])['state'] == "done":

                                    try:
                                        BTC_buy = self.upbit.buy_market_order("KRW-BTC", qty * market_ask)  # BTC 쓴만큼 시장가로 다시 구매(매수금액)
                                        if BTC_buy == None:
                                            print("BTC구매불가 - KRW잔액부족")
                                            print("오류내용 - {}".format(BTC_buy))
                                            print("-------쓰레드중지--------")
                                            get_trade.close()
                                            return False
                                    except:
                                        print("BTC구매실패 - 알 수 없는 오류")
                                        print("-------쓰레드중지--------")
                                        get_trade.close()
                                else:
                                    print("업비트 일부 미체결 되었습니다")
                                    get_trade.close()
                                    self.tele.alarm_command("c")
                                    return False

                            elif type(upbSellBuyError) != dict:  # 제대로 체결되지 않으면
                                print("upbSellBuyError 오류 = 체결실패")
                                print("오류내용 : {}".format(upbSellBuyError))
                                self.bithumb.buy_limit_order(self.ticker, market_bid,qty)  # 매수 정상적으로 처리 안되면 판 물량만큼 재매수대기 건다
                                print("-------쓰레드중지--------")
                                get_trade.close()
                                return False

                            print("거래완료")
                            self.tele.alarm_command("a")

                    #TODO bithumb 매수/upbit 매도
                    elif KRW_upb_bid - bit_ask >= bit_ask * margin:  #
                        perc2 = (KRW_upb_bid / bit_ask) - 1
                        market_ask = bit_ask  #

                        if upb_bid_qty < qty or bit_ask_qty < qty:  #
                            print(formatDate + "시장수량부족")
                            return False
                        if bithumbAvailableKRW < market_ask * qty:
                            print(formatDate + "빗썸 현금부족")
                            return False

                        after_upbitAvailableCur = float(self.upbit.get_balance(self.ticker2))

                        if round(after_upbitAvailableCur, 4) < qty:
                            print(formatDate + "업비트 현물부족")
                            return False
                        # ---------------------------------------------

                        if bithumbAvailableKRW >= market_ask * qty and after_upbitAvailableCur >= qty:
                            print("가격차이비율 : {}%".format(round(perc2, 4) * 100))
                            print(formatDate + "   빗썸 {}원 구매 + 업비트 {}원 판매".format(bit_ask, math.trunc(KRW_upb_bid)))
                            bithumbSellBuyError = self.bithumb.buy_limit_order(self.ticker, market_ask, qty)

                            # -----------------체결 성공시 미체결조회주문------------------
                            if bithumbSellBuyError['status'] == "0000":  # 체결 성공하면
                                order_desc2 = ('bid', self.ticker, bithumbSellBuyError['order_id'], 'KRW')
                                after_bitAvailableCur = float(self.bithumb.get_balance(self.ticker)[0])
                                after_bitAvailableKRW = self.bithumb.get_balance(self.ticker)[2]

                                if math.isclose(bithumbAvailableCur + qty, after_bitAvailableCur) or \
                                        bithumbAvailableKRW > after_bitAvailableKRW:  # 거래 정상 진행시
                                    pass
                                elif math.isclose(bithumbAvailableCur, after_bitAvailableCur) or \
                                        after_bitAvailableKRW == bithumbAvailableKRW:
                                    # 전량 미체결 시 (기존pci잔고 = 거래후 pci 잔고)
                                    self.bithumb.cancel_order(order_desc2)  # 주문취소
                                    print("주문 취소 : {사유} = 빗썸체결실패 ")
                                    get_trade.close()
                                    time.sleep(2)
                                    self.alive = True
                                    return False
                                else:  # 일부 미체결시
                                    print("주문 취소 : {사유} = 빗썸일부미체결 ")
                                    get_trade.close()
                                    print("-------쓰레드중지--------")
                                    self.tele.alarm_command("d")
                                    return False
                            elif bithumbSellBuyError['status'] != "0000":  # 매수 과정에서 오류 발생시 바로 False 리턴해서 while문 종료시킴
                                print("bithumbSellBuyError 오류")
                                print("오류내용 : {}".format(bithumbSellBuyError))
                                print("-------쓰레드중지--------")
                                self.tele.alarm_command("e")
                                get_trade.close()
                                return False

                            upbSellBuyError = self.upbit.sell_limit_order(self.ticker2, upb_bid, qty)
                            # TODO upbSellBuyError이 정상적으로 처리되어도 after_upbit...로 PCI잔고조회했을때 반영이 되지 않는 오류가 있음
                            after_upbitAvailableCur = float(self.upbit.get_balance(self.ticker2))  # 거래 후 잔량
                            after_upbBTC_bal = self.upbit.get_balance("BTC")
                            # ---------------체결 정상적으로 진행되면 미체결조회---------------
                            if type(upbSellBuyError) == dict:
                                # 코인 수 변화있거나, BTC잔액 변화있거나, 주문상태가 done이라면 == 정상주문 진행되었다면,
                                if math.isclose(upbitAvailableCur - qty, after_upbitAvailableCur) or \
                                        upbitAvailableBTC != after_upbBTC_bal or self.upbit.get_order(upbSellBuyError['uuid'])['state'] == "done":
                                    try:
                                        BTC_buy = self.upbit.sell_market_order("KRW-BTC", qty * upb_bid)  # BTC 쓴만큼 시장가로 다시 판매(팔 비트 개수입력)
                                        if BTC_buy == None:
                                            print("BTC구매불가 - KRW잔액부족")
                                            print("오류내용 - {}".format(BTC_buy))
                                            print("-------쓰레드중지--------")
                                            get_trade.close()
                                            return False
                                    except:
                                        print("BTC구매실패 - 알 수 없는 오류")
                                        print("-------쓰레드중지--------")
                                        get_trade.close()
                                        return False
                                else:
                                    print("업비트 미체결 되었습니다")
                                    get_trade.close()
                                    self.tele.alarm_command("c")
                                    return False
                            elif type(upbSellBuyError) != dict:  # 제대로 체결되지 않으면
                                print("upbSellBuyError 오류 = 체결실패")
                                print("오류내용 : {}".format(upbSellBuyError))
                                self.bithumb.sell_limit_order(self.ticker, market_ask, qty)  # 업빗에서 매도 오류시 빗썸에서 산 물량만큼 재매도대기 건다
                                get_trade.close()
                                print("-------쓰레드중지--------")
                                return False
                            print("거래완료")
                            self.tele.alarm_command("b")
                    else:
                        print(formatDate + "가격차이 탐지중")

                else:
                    print(data)
                    get_trade.close()
                    return False

            except TypeError:
                print("TradeCurrencyWorker / data 가져오기 실패 : TypeError 발생")
                return False

    def close(self):
        self.alive = False


if __name__ == "__main__":
    ticker, ticker2 = input("빗썸 티커,업비트 티커 : ").split(",")
    qty, margin = map(float, input("qty , margin : ").split(","))
    get_trade = TradeCurrencyWorker(ticker, ticker2)
    get_trade.run()
