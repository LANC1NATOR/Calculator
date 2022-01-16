import datetime as dt


class Record:

    def __init__(self, amount, comment='Без комментария', date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)


    def get_today_stats(self):
        date_today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == date_today)

    def get_week_stats(self):
        date_today = dt.date.today()
        week_delta = date_today - dt.timedelta(days=6)
        return sum(record.amount for record in self.records
                   if week_delta <= record.date <= date_today)


class CashCalculator(Calculator):
    USD_RATE = 74.29
    EURO_RATE = 84.07
    RUB_RATE = 1.0

    def get_today_cash_remained(self, currency):
        currencies = {
            'rub': (self.RUB_RATE, 'руб'),
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro')
        }
        rest = self.limit - self.get_today_stats()
        rate, currency_name = currencies[currency]
        rest_in_currency = abs(round(rest / rate, 2))
        if rest > 0:
            if currency in currencies:
                return f'На сегодня осталось ' \
                       f'{rest_in_currency} {currency_name}'
            else:
                return 'Валюта не поддерживается'
        elif rest == 0:
            return 'Денег нет, держись'
        else:
            if currency in currencies:
                return f'Денег нет, держись: твой долг - ' \
                       f'{rest_in_currency} {currency_name}'
            else:
                return 'Валюта не поддерживается'




class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        rest = self.limit - self.get_today_stats()
        if rest > 0:
            return f'Сегодня можно съесть что-нибудь ещё, ' \
                   f'но с общей калорийностью не более {rest} кКал'
        else:
            return 'Хватит есть!'


if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment="кофе"))
    cash_calculator.add_record(Record(amount=356, comment="Серёге за обед"))
    cash_calculator.add_record(
        Record(amount=3000, comment="бар в Танин др", date="09.01.2023"))
    print(cash_calculator.get_today_cash_remained(currency='usd'))

    calorie_calculator = CaloriesCalculator(5000)
    calorie_calculator.add_record(Record(amount=455))
    calorie_calculator.add_record(Record(amount=655))
    calorie_calculator.add_record(Record(amount=1240))
    print(calorie_calculator.get_calories_remained())

