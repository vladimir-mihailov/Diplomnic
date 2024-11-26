import requests
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb

# Словарь кодов валют и их полных названий
currencies = {
    "BTC": "Биткойн",
    "ETH": "Эфириум",
    "SOL": "Солана",
    "BNB": "БНБ",
    "XRP": "XRP",
    "DOGE":"Догекоин",
    "USDC":"USDC",
    "TRX": "ТРОН",
}

currencies1= {
    "USD": "Американский доллар",
    "EUR": "Евро",
    "JPY": "Японская йена",
    "GBP": "Британский фунт стерлингов",
    "CAD": "Канадский доллар",
    "CHF": "Швейцарский франк",
    "CNY": "Китайский юань",
    "RUB": "Российский рубль",
}


def update_b_label(event):
    code = base_combobox.get()
    name = currencies.get(code, "Неизвестная валюта")
    b_label.config(text=name)

def update_t_label(event):
    code = target_combobox.get()
    name = currencies1.get(code, "Неизвестная валюта")
    t_label.config(text=name)

def exchange():
    base_code = base_combobox.get()
    target_code = target_combobox.get()

    if base_code and target_code:
        try:
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={crypto_name}&vs_currencies=usd{base_code}.json')
            response.raise_for_status()

            data = response.json()
            exchange_rate = data['bpi'].get(target_code, {}).get('rate_float')

            if exchange_rate is not None:
                base = currencies[base_code]
                target = currencies[target_code]
                mb.showinfo("Курс обмена", f"Курс 1 {base} = {exchange_rate:.2f} {target}")
            else:
                mb.showerror("Ошибка", f"Курс для валюты {target_code} не найден.")
        except requests.exceptions.RequestException as e:
            mb.showerror("Ошибка", f"Проблема с подключением: {e}")
        except Exception as e:
            mb.showerror("Ошибка", f"Ошибка: {e}")
    else:
        mb.showwarning("Внимание", "Выберите коды валют.")

def reset_selection():
    base_combobox.set('')
    target_combobox.set('')
    b_label.config(text='')
    t_label.config(text='')

# Создание графического интерфейса
window = Tk()
window.title("Курс биткойна <<Меняла>>")
window.geometry("400x360")

Label(text="Биткойн:").pack(padx=10, pady=5)
base_combobox = ttk.Combobox(values=list(currencies.keys()), state="readonly")
base_combobox.pack(padx=10, pady=5)
base_combobox.bind("<<ComboboxSelected>>", update_b_label)

b_label = ttk.Label()
b_label.pack(padx=10, pady=10)

Label(text="Целевая валюта:").pack(padx=10, pady=5)
target_combobox = ttk.Combobox(values=list(currencies1.keys()), state="readonly")
target_combobox.pack(padx=5, pady=5)
target_combobox.bind("<<ComboboxSelected>>", update_t_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=5)

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)
Button(text="Сбросить выбор", command=reset_selection).pack(padx=10, pady=10)

window.mainloop()