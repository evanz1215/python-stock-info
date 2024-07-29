class Stock:
    def __init__(self, company_code, company_name, date, time, content):
        self.company_code = company_code
        self.company_name = company_name
        self.date = date
        self.time = time
        self.content = content

    def __str__(self):
        return f"{self.company_code} {self.company_name} {self.date} {self.time} {self.content}"
