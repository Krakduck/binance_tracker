import requests
import customtkinter as ct
from database_for_binance_tracker import BinanceDatabase

class Card:
    def __init__(self, name, frame):
        self.name = name
        self.frame=frame #ct.CTkFrame(mainFrame, width=200, height=280, fg_color="#2f3440")
        self.frame.pack(side="left", padx=10, pady=10)
        self.frame.pack_propagate(False)

        self.name_label = ct.CTkLabel(self.frame, text=self.name.upper(), font=('Arial', 28, 'bold'))
        self.amount = ct.CTkLabel(self.frame, text=f'0.0 {self.name}', font=('Arial', 18))
        self.to_dollar = ct.CTkLabel(self.frame, text='0.0 $', font=('Arial', 18))
        self.to_ruble = ct.CTkLabel(self.frame, text='0.0 ₽', font=('Arial', 18))
        self.calculate = ct.CTkButton(self.frame, text=f'РАССЧИТАТЬ {self.name.upper()}', fg_color='#359af0', text_color='white', width=180,height=35, font=('Arial', 14, 'bold'), command=lambda: self.calc())
        self.sell_val = ct.CTkButton(self.frame, text=f'ОБНУЛИТЬ {self.name.upper()}', fg_color='#f03535', text_color='white', width=15,height=25, font=('Arial', 14, 'bold'), command=lambda: self.sell())

        self.name_label.pack(padx=10, pady=10)
        self.amount.pack(padx=10, pady=5)
        self.to_dollar.pack(padx=10, pady=5)
        self.to_ruble.pack(padx=10, pady=10) #менеджер для чтения md
        self.calculate.pack(padx=10, pady=5)
        self.sell_val.pack(padx=10, pady=10)

    def sell(self):
        try:
            db.delete(self.name)
            sostoyanie.configure(text='Монета продана!')
        except Exception as e:
            print(e)

    def calc(self):
        try:
            # 1. Получаем курс доллара (делаем запрос ВНУТРИ функции, чтобы данные были свежими)
            res_cbr = requests.get("https://www.cbr-xml-daily.ru/daily_json.js")
            print(f'res_cbr {res_cbr}')
            usd_to_rub = res_cbr.json()['Valute']['USD']['Value']
            print(f'usd_to_rub {usd_to_rub}')
            symbol = f"{self.name}USDT"
            print(f'symbol {symbol}')
            res_binance = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
            print(f'res_binance {res_binance}')
            price_now = res_binance.json()['price']
            print(f'price_now {price_now}')

            info = db.get(self.name)
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
            if profit < 0:
                color = '#f41c2c'
            else:
                color = '#2eee3b'

            print('рассчитано')
            self.amount.configure(text=f'{amount} btc')
            self.to_dollar.configure(text=f"{profit:.2f} $", text_color=color)
            self.to_ruble.configure(text=f"{profit_ruble:.2f} ₽", text_color=color)

        except Exception as e:
            print(e)

class AddTransaction:
    def __init__(self, frame):
        self.frame =frame #ct.CTkFrame(mainFrame, width=200, height=280, fg_color="#2f3440")
        self.frame.pack(padx=10)
        self.frame.pack_propagate(False)

        self.menu = ct.CTkOptionMenu(self.frame, values=["BTC", "ETH", "BNB"], width=100)
        self.entry_amount = ct.CTkEntry(self.frame, placeholder_text="Количество", font=('Arial', 14, 'bold'), width=150)
        self.entry_price = ct.CTkEntry(self.frame, placeholder_text="Цена покупки", font=('Arial', 14, 'bold'), width=150)
        self.text = ct.CTkLabel(self.frame, text='добавить покупку', font=('Arial', 20, 'bold'))
        self.add = ct.CTkButton(self.frame, text='добавить', fg_color='#359af0', text_color='white', width=200,font=('Arial', 17, 'bold'), command=lambda: self.add_trans())

        self.text.pack(padx=10, pady=10, anchor="w")
        self.menu.pack(pady=10, padx=10, side="left")
        self.entry_amount.pack(pady=10, padx=10, ipady=8, side="left")
        self.entry_price.pack(pady=10, padx=10, ipady=8, side="left")
        self.add.pack(pady=10, padx=10, ipady=8, side="left")

    def add_trans(self):
        try:
            name_valut = self.menu.get()
            print(name_valut)
            db.add(name_valut, float(self.entry_amount.get()),
                   float(self.entry_price.get()))  # could not convert string to float: '.!ctkframe2.!ctkentry'
            sostoyanie.configure(text='Покупка успешно добавлена!')
            self.entry_amount.delete(0, 'end')
            self.entry_price.delete(0, 'end')
        except Exception as e:
            print(e)

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
btc = Card('BTC',frameBTC)

frameBNB = ct.CTkFrame(mainFrame, width=200,height=280,fg_color="#2f3440")
bnb = Card('BNB',frameBNB)

frameETH = ct.CTkFrame(mainFrame, width=200,height=280,fg_color="#2f3440")
eth = Card('ETH',frameETH)

frameADD = ct.CTkFrame(window,fg_color="#2f3440",width=640,height=100)
add = AddTransaction(frameADD)

sostoyanie =ct.CTkLabel(window,text='Состояние:',font=('Arial', 20, 'bold'))
sostoyanie.pack(pady=10,padx=10,ipady=8,side="left")

window.mainloop()
