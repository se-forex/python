import matplotlib.pyplot as plt
from matplotlib.finance import quotes_historical_yahoo_ochl, candlestick_ochl
from matplotlib.dates import YearLocator, MonthLocator, DateFormatter
import datetime

date1 = datetime.date(2017, 1, 1)     # Начальная дата.
date2 = datetime.date(2017, 12, 31)   # Конечная дата.

years = YearLocator()    # Ежегодная сетка.
months = MonthLocator()  # Ежемесячная сетка.
yearsFmt = DateFormatter('%Y')  # Форматная строка для оси абсцисс (только год).

quotes = quotes_historical_yahoo_ochl('AAPL', date1, date2) # Получили котировки.
if len(quotes) == 0:   # Если ничего не получено.
    raise SystemExit

# dates = [q[0] for q in quotes]    # Можно выделить только даты
# closes = [q[2] for q in quotes]   # и только цены закрытия.

fig, ax = plt.subplots()            # Создали график.
# ax.plot_date(dates, closes, '-', color='b')   # Линия по ценам закрытия.
candlestick_ochl(ax, quotes, width=0.6, colorup='g', colordown='r') # Свечной график.

ax.xaxis.set_major_locator(years)      # Установили шаг делений по оси абсцисс
ax.xaxis.set_major_formatter(yearsFmt) # и формат надписей.
ax.xaxis.set_minor_locator(months)
ax.autoscale_view()

# Функция для форматирования текущей ординаты в строке состояния:
def price(x):
    return '$%1.2f'%x

ax.fmt_xdata = DateFormatter('%Y-%m-%d')  # Формат для текущей абсциссы в строке состояния.
ax.fmt_ydata = price                      # Формат для текущей ординаты в строке состояния.
ax.grid(True)                             # Показывать сетку.

fig.autofmt_xdate()
plt.show()
