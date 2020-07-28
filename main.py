from tkinter import *
from tkinter import ttk
import currency
from decimal import Decimal


def convert():
    bank = bank_tk.get()
    # TODO принимать числа с запятой
    amount = Decimal(amount_tk.get())
    curr_from = curr_from_tk.get()
    curr_to = curr_to_tk.get()
    date = date_entry.get()
    # TODO отдавать числа в формате с разрядами и запятой
    result = currency.choose_bank(bank, amount, curr_from, curr_to, date)
    label['text'] = f'По курсу {bank} на {date}, {amount} {curr_from} = {result} {curr_to}'


root = Tk()
root.title('Конвертер валют (ЦБ РФ / НБ РБ)')
root.geometry('400x240')
root.resizable(False, False)
Grid.rowconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 0, weight=1)
# root.columnconfigure(0, weight=1)
# root.rowconfigure(0, weight=1)

# mainframe = Frame(root)
# mainframe.grid(column=0, row=0)

banks_list = ['ЦБ РФ', 'НБ РБ']

Label(text='Банк').grid(row=0, column=0)
bank_tk = StringVar(root)
bank_tk.set(banks_list[0])
bank_tk_list = OptionMenu(root, bank_tk, *banks_list)
bank_tk_list.config(width=5)
bank_tk_list.grid(row=0, column=1)

Label(text='Сумма').grid(row=1, column=0)
amount_tk = Entry(root)
amount_tk.grid(row=1, column=1)

currency_list = ['RUB', 'AUD', 'AZN', 'GBP', 'AMD', 'BYN', 'BGN', 'BRL', 'HUF', 'HKD', 'DKK', 'USD', 'EUR', 'INR',
                 'KZT', 'CAD', 'KGS', 'CNY', 'MDL', 'NOK', 'PLN', 'RON', 'XDR', 'SGD', 'TJS', 'TRY', 'TMT', 'UZS',
                 'UAH', 'CZK', 'SEK', 'CHF', 'ZAR', 'KRW', 'JPY', 'BYR', 'IRR', 'ISK', 'KWD', 'NZD']

Label(text='Из').grid(row=2, column=0)
curr_from_tk = StringVar(root)
curr_from_tk.set(currency_list[0])
curr_to_list = OptionMenu(root, curr_from_tk, *currency_list)
curr_to_list.config(width=3)
curr_to_list.grid(row=2, column=1)

Label(text='В').grid(row=3, column=0)
curr_to_tk = StringVar(root)
curr_to_tk.set((currency_list[11]))
curr_from_list = OptionMenu(root, curr_to_tk, *currency_list)
curr_from_list.config(width=3)
curr_from_list.grid(row=3, column=1)

Label(text='Дата').grid(row=4, column=0, pady=5)
date_entry = Entry(root)
date_entry.grid(row=4, column=1)

calculate = Button(root, text='Сконвертировать', command=convert)
calculate.grid(row=6, column=2)

empty_label = Label(root)
empty_label.grid(row=5, column=3)

label = Label(root, text='По курсу [БАНК] на [ДАТА], [CУММА] [ИЗ] = [РЕЗУЛЬТАТ] [В]')
label.grid(row=7, column=0, columnspan=3, sticky=N+S+E+W, ipady=10)

root.mainloop()
