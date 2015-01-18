name = 'Standard Chartered'

form_url = ('https://ebank.standardchartered.com.tw/HIB/servlet/'
            'HttpDispatcher/Login/prompt')

login_url = ('https://ebank.standardchartered.com.tw/HIB/servlet/'
             'HttpDispatcher/Login/login')

balance_url = ('https://ebank.standardchartered.com.tw/HIB/servlet/'
               'HttpDispatcher/BnkSrv/rslt')

logout_url = ('https://ebank.standardchartered.com.tw/HIB/servlet/'
              'HttpDispatcher/Logout/logout')

credentials = (
    ('ID card number', 'custId'),
    ('Username', 'userId'),
    ('Password', 'password'),
)


def get_form_data(html, credentials):
    form_data = {
        'locale': 'en_US'
    }
    form_data.update(credentials)
    return form_data


def parse_balance(html):
    accounts = html.xpath(
        '//div[@id="right_con"]/table/tr[position()>2]/td[last()-2]/a/text()')
    currencies = html.xpath(
        '//div[@id="right_con"]/table/tr[position()>2]/td[last()-1]/text()')
    amounts = html.xpath(
        '//div[@id="right_con"]/table/tr[position()>2]/td[last()]/text()')

    data = []
    for account, currency, amount in zip(accounts, currencies, amounts):
        data.append((account, currency, amount))
    return data
