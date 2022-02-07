import datetime as dt


class Record:

    def __init__(self, amount, comment='No comment', date=None):
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
                return f'Left for today: ' \
                       f'{rest_in_currency} {currency_name}'
            else:
                return 'Currency not supported'
        elif rest == 0:
            return 'No money left'
        else:
            if currency in currencies:
                return f'There is no money left: your debt - ' \
                       f'{rest_in_currency} {currency_name}'
            else:
                return 'Currency not supported'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        rest = self.limit - self.get_today_stats()
        if rest > 0:
            return f'You can eat some more today, ' \
                   f'but with a total calorie content of no more than' \
                   f' {rest} kcal'
        else:
            return 'Stop eating!'


if __name__ == '__main__':
    cash_calculator = CashCalculator(1000)
    cash_calculator.add_record(Record(amount=145, comment="coffee"))
    cash_calculator.add_record(Record(amount=356, comment="to Mary for lunch"))
    cash_calculator.add_record(
        Record(amount=3000, comment="drinks on a party", date="09.01.2023"))
    print(cash_calculator.get_today_cash_remained(currency='usd'))

    calorie_calculator = CaloriesCalculator(5000)
    calorie_calculator.add_record(Record(amount=455))
    calorie_calculator.add_record(Record(amount=655))
    calorie_calculator.add_record(Record(amount=1240))
    print(calorie_calculator.get_calories_remained())
