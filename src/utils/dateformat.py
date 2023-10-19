import datetime

class DateFormat():

    @classmethod
    def convert_date(self,date):
        return datetime.datetime.strftime(date, '%d/%m/%Y')
    
    @classmethod
    def convert_date_hour(cls, date):
        return datetime.datetime.strftime(date, '%d/%m/%Y %H:%M:%S')