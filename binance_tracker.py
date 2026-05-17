

import requests
import customtkinter as ct
from database_for_binance_tracker import BinanceDatabase



db = BinanceDatabase()
# Настройка темы
ct.set_appearance_mode("dark")  # Варианты: "System", "Dark", "Light"
ct.set_default_color_theme("dark-blue")  # Варианты: "blue", "green", "dark-blue"

window = ct.CTk()
window.geometry("800x500")
window.title("Binance Tracker")

mainFrame=ct.CTkFrame(window,height=600,fg_color="transparent") # прозрачный, чтобы не выделялся
mainFrame.pack(pady=10, padx=10)

frameBTC = ct.CTkFrame(mainFrame, width=200,height=280,fg_color="#2f3440")
frameBTC.pack(side="left", padx=10,pady=10)
frameBTC.pack_propagate(False)

frameBNB = ct.CTkFrame(mainFrame, width=200,height=280,fg_color="#2f3440")
frameBNB.pack(side="left", padx=10,pady=10)
frameBNB.pack_propagate(False)

frameETH = ct.CTkFrame(mainFrame, width=200,height=280,fg_color="#2f3440")
frameETH.pack(side="left", padx=10,pady=10)
frameETH.pack_propagate(False)

frameADD = ct.CTkFrame(window,fg_color="#2f3440",width=640,height=100)
frameADD.pack(padx=10)
frameADD.pack_propagate(False)



def addtrans():
    try:
        nameValut=menu.get()
        print(nameValut)
        db.add(nameValut,float(entryAmount.get()),float(entryPrice.get()))  #could not convert string to float: '.!ctkframe2.!ctkentry'
        sostoyanie.configure(text = 'Покупка успешно добавлена!')
        entryAmount.delete(0, 'end')
        entryPrice.delete(0, 'end')
    except Exception as e:
        print(e)


def sell(s):
    try:
        db.delete(s)
        sostoyanie.configure(text = 'Монета продана!')
    except Exception as e:
        print(e)

def calc(coin):
    try:
        # 1. Получаем курс доллара (делаем запрос ВНУТРИ функции, чтобы данные были свежими)
        res_cbr = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
        print(f'res_cbr {res_cbr}')
        usd_to_rub = res_cbr.json()['Valute']['USD']['Value']
        print(f'usd_to_rub {usd_to_rub}')
        symbol = f"{coin}USDT"
        print(f'symbol {symbol}')
        res_binance = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
        print(f'res_binance {res_binance}')
        price_now = res_binance.json()['price']
        print(f'price_now {price_now}')

        info = db.get(coin)
        print(f'info {info}')
        price = 0
        amount = 0
        zatrati = 0
        for i in info:
            print(f'i in info {i}')
            amount += i[1]
            price += i[2]
            zatrati += i[1] * i[2]

        profit = float(price_now) * amount - zatrati
        print(f'profit {profit}')
        profit_ruble = profit * usd_to_rub
        print(f'profit_ruble {profit_ruble}')
        if profit<0:
            color = '#f41c2c'
        else:
            color = '#2eee3b'
        if coin=='BTC':
            print('рассчитано')
            amountBTC.configure(text=f'{amount} btc')
            BTC_to_dollar.configure(text=f"{profit:.2f} $", text_color=color)
            BTC_to_ruble.configure(text=f"{profit_ruble:.2f} ₽", text_color=color)
        elif coin=='ETH':
            print('рассчитано')
            amountETH.configure(text=f'{amount} eth')
            ETH_to_dollar.configure(text=f"{profit:.2f} $", text_color=color)
            ETH_to_ruble.configure(text=f"{profit_ruble:.2f} ₽", text_color=color)
        else:
            print('рассчитано')
            amountBNB.configure(text=f'{amount} bnb')
            BNB_to_dollar.configure(text=f"{profit:.2f} $", text_color=color)
            BNB_to_ruble.configure(text=f"{profit_ruble:.2f} ₽", text_color=color)
    except Exception as e:
        print(e)




nameBTC = ct.CTkLabel(frameBTC,text='BTC',font=('Arial', 28, 'bold'))
amountBTC = ct.CTkLabel(frameBTC,text='0.0 btc',font=('Arial', 18))
BTC_to_dollar =ct.CTkLabel(frameBTC,text='0.0 $',font=('Arial', 18))
BTC_to_ruble = ct.CTkLabel(frameBTC,text='0.0 ₽',font=('Arial', 18))
calculateBTC = ct.CTkButton(frameBTC, text='РАССЧИТАТЬ BTC', fg_color='#359af0', text_color='white', width=180,height=35, font=('Arial', 14, 'bold'), command=lambda: calc('BTC'))
sellBTC = ct.CTkButton(frameBTC, text='ОБНУЛИТЬ BTC', fg_color='#f03535', text_color='white', width=15,height=25, font=('Arial', 14, 'bold'), command=lambda: sell('BTC'))

nameBTC.pack(padx=10, pady=10)
amountBTC.pack(padx=10, pady=5)
BTC_to_dollar.pack(padx=10, pady=5)
BTC_to_ruble.pack(padx=10, pady=10)
calculateBTC.pack(padx=10, pady=5)
sellBTC.pack(padx=10, pady=10)



nameBNB = ct.CTkLabel(frameBNB,text='BNB',font=('Arial', 28, 'bold'))
amountBNB = ct.CTkLabel(frameBNB,text='0.0 bnb',font=('Arial', 18))
BNB_to_dollar =ct.CTkLabel(frameBNB,text='0.0 $',font=('Arial', 18))
BNB_to_ruble = ct.CTkLabel(frameBNB,text='0.0 ₽',font=('Arial', 18))
calculateBNB = ct.CTkButton(frameBNB, text='РАССЧИТАТЬ BNB', fg_color='#359af0', text_color='white', width=180,height=35, font=('Arial', 14, 'bold'), command=lambda: calc('BNB'))
sellBNB = ct.CTkButton(frameBNB, text='ОБНУЛИТЬ BNB', fg_color='#f03535', text_color='white', width=15,height=25, font=('Arial', 14, 'bold'), command=lambda: sell('BNB'))

nameBNB.pack(padx=10, pady=10)
amountBNB.pack(padx=10, pady=5)
BNB_to_dollar.pack(padx=10, pady=5)
BNB_to_ruble.pack(padx=10, pady=10)
calculateBNB.pack(padx=10, pady=5)
sellBNB.pack(padx=10, pady=10)



nameETH = ct.CTkLabel(frameETH,text='ETH',font=('Arial', 28, 'bold'))
amountETH = ct.CTkLabel(frameETH,text='0.0 eth',font=('Arial', 18))
ETH_to_dollar =ct.CTkLabel(frameETH,text='0.0 $',font=('Arial', 18))
ETH_to_ruble = ct.CTkLabel(frameETH,text='0.0 ₽',font=('Arial', 18))
calculateETH = ct.CTkButton(frameETH, text='РАССЧИТАТЬ ETH', fg_color='#359af0', text_color='white', width=180,height=35, font=('Arial', 14, 'bold'), command=lambda: calc('ETH'))
sellETH = ct.CTkButton(frameETH, text='ОБНУЛИТЬ ETH', fg_color='#f03535', text_color='white', width=15,height=25, font=('Arial', 14, 'bold'), command=lambda: sell('ETH'))

nameETH.pack(padx=10, pady=10)
amountETH.pack(padx=10, pady=5)
ETH_to_dollar.pack(padx=10, pady=5)
ETH_to_ruble.pack(padx=10, pady=10)
calculateETH.pack(padx=10, pady=5)
sellETH.pack(padx=10, pady=10)



text = ct.CTkLabel(frameADD,text='добавить покупку',font=('Arial', 20, 'bold'))
menu = ct.CTkOptionMenu(frameADD,values=["BTC", "ETH", "BNB"],width=100)
entryAmount = ct.CTkEntry(frameADD, placeholder_text="Количество",font=('Arial', 14, 'bold'), width=150)
entryPrice = ct.CTkEntry(frameADD, placeholder_text="Цена покупки",font=('Arial', 14, 'bold'), width=150)
add = ct.CTkButton(frameADD, text='добавить', fg_color='#359af0', text_color='white', width=200, font=('Arial', 17, 'bold'), command=lambda: addtrans())

text.pack(padx=10, pady=10,anchor="w")
menu.pack(pady=10,padx=10,side="left")
entryAmount.pack(pady=10,padx=10,ipady=8,side="left")
entryPrice.pack(pady=10,padx=10,ipady=8,side="left")
add.pack(pady=10,padx=10,ipady=8,side="left")

sostoyanie =ct.CTkLabel(window,text='Состояние:',font=('Arial', 20, 'bold'))
sostoyanie.pack(pady=10,padx=10,ipady=8,side="left")





#padx / pady (используются в .pack() или .grid()): Это внешние отступы. Они расталкивают виджеты друг от друга. ipadx / ipady (Internal Padding): Это внутренние отступы. Они увеличивают размер самого виджета изнутри (например, делают кнопку шире или выше, увеличивая расстояние от текста до края рамки).
#Дело в том, что метод .pack() работает по принципу «упаковки чемодана». По умолчанию он выделяет для виджета всю ширину окна и центрирует его в этом пространстве. Аргумент anchor определяет, к какой стороне света «приклеить» виджет внутри выделенной ему области. Используются сокращения от сторон света (на английском):
#Когда вы указываете side="left", вы меняете логику «упаковки». Теперь каждый новый виджет не занимает всю свободную строку сверху вниз, а встает в очередь слева направо.
#Если вам нужно строгое табличное расположение, забудьте про .pack() и используйте .grid(). Это как таблица в Excel, где вы сами указываете номер строки (row) и колонки (column). btn1.grid(row=0, column=0, padx=10)
#Часто бывает нужно, чтобы часть интерфейса была в ряд (например, панель кнопок), а всё остальное — друг под другом. Для этого кнопки кладут в «коробку» (CTkFrame).
#frame = ctk.CTkFrame(app)
#frame.pack(fill="x", padx=10, pady=10)
#btn_ok = ct.CTkButton(frame, text="ОК")
#btn_ok.pack(side="left", padx=5)




window.mainloop()