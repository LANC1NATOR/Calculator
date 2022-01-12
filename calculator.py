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
        if record.date > dt.datetime.now().date():
            print('Мы не делаем записи наперед')
        else:
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

    def get_today_cash_remained(self, currency='rub'):
        rest = self.limit - self.get_today_stats()
        if rest > 0:
            if currency == 'rub':
                return f'На сегодня осталось {rest} руб'
            elif currency == 'usd':
                return f'На сегодня осталось ' \
                       f'{round(rest / CashCalculator.USD_RATE, 2)} USD'
            elif currency == 'eur':
                return f'На сегодня осталось ' \
                       f'{round(rest / CashCalculator.EURO_RATE, 2)} Euro'
            else:
                return 'Валюта не поддерживается'
        elif rest == 0:
            return 'Денег нет, держись'
        else:
            if currency == 'rub':
                return f'Денег нет, держись: твой долг - {rest} руб'
            elif currency == 'usd':
                return f'Денег нет, держись: твой долг - ' \
                       f'{round(rest / CashCalculator.USD_RATE, 2)} USD'
            elif currency == 'eur':
                return f'Денег нет, держись: твой долг - ' \
                       f'{round(rest / CashCalculator.EURO_RATE, 2)} Euro'
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
        Record(amount=3000, comment="бар в Танин др", date="09.01.2022"))
    print(cash_calculator.get_today_cash_remained('rub'))

    calorie_calculator = CaloriesCalculator(5000)
    calorie_calculator.add_record(Record(amount=455))
    calorie_calculator.add_record(Record(amount=655))
    calorie_calculator.add_record(Record(amount=1240))
    print(calorie_calculator.get_calories_remained())
