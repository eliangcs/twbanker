from base64 import b64encode
from hashlib import sha1


name = 'First Bank'

form_url = 'https://ibank.firstbank.com.tw/NetBank/index.html'

login_url = 'https://ibank.firstbank.com.tw/NetBank/login.html'

balance_url = 'https://ibank.firstbank.com.tw/NetBank/1/00_rs.html'

logout_url = 'https://ibank.firstbank.com.tw/NetBank/logout.html'

logout_method = 'post'

credentials = (
    ('ID card number', 'loginCustId'),
    ('Username', 'usrId'),
    ('Password', 'pwd'),
)


def get_form_data(html, credentials):
    form_data = {
        'loginCustIdRptSeq': '0',
        'countInt': '3',
        'countLo': '5',
        'countUp': '0',
        'browser': 'CHROME 39.0.2171.99',
        'osType': 'Mac OS',
        'loginType': '0',
        'loginStts': '0',
        'h1': '',
        'noneLg': 'Y',
        'macAddressFromCOM': '',
        'macOS': 'MacIntel',
        'show': '0',
        'showNotice': '123...'
    }
    form_data.update(credentials)
    form_data['pwd'] = b64encode(sha1(
        credentials['loginCustId'] + '0' + credentials['pwd']).digest())
    return form_data


def parse_balance(html):
    amounts = html.xpath('//tr[count(td)=10][position()>1]/td[6]/text()')
    accounts = html.xpath('//tr[count(td)=10][position()>1]/td[3]/a/text()')

    data = []
    for account, amount in zip(accounts, amounts):
        account = account.strip()
        amount = amount.strip()
        try:
            float(amount.replace(',', ''))
            int(account)
        except ValueError:
            pass
        else:
            # TODO: Foreign currency
            data.append((account, 'TWD', amount))
    return data
