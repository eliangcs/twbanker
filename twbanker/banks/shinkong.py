import re

from lxml import html as _html


name = 'Shin Kong Bank'

form_url = 'https://ibank.skbank.com.tw/nbank/membership/login.aspx'

login_url = 'https://ibank.skbank.com.tw/nbank/membership/login.aspx'

balance_url = ('https://ibank.skbank.com.tw/nBank/DesktopDefault.aspx?'
               'TabId=479&CC=CT0101801&F=1&&mid=717&'
               'desktopsrc=~%2fDesktopModules%2fNetBank%2fCT0101801.ascx')

logout_url = ('https://ibank.skbank.com.tw/nBank/DesktopDefault.aspx?'
              'TabId=479&CC=CT0101801&F=1&&mid=717&'
              'desktopsrc=%7e%2fDesktopModules%2fNetBank%2fCT0101801.ascx')

logout_method = 'post'

user_agent = 'twbanker'

credentials = (
    ('ID card number',
        'ctl00$ContentPlaceHolder1$ctl00$ctl00$skbLogin$UserName'),
    ('Username',
        'ctl00$ContentPlaceHolder1$ctl00$ctl00$skbLogin$txtUserAlias'),
    ('Password',
        'ctl00$ContentPlaceHolder1$ctl00$ctl00$skbLogin$Password'),
)


def get_form_data(html, credentials, session):
    form_data = {
        '__EVENTVALIDATION': html.xpath(
            '//input[@id="__EVENTVALIDATION"]/@value')[0],
        '__VIEWSTATE': html.xpath('//input[@id="__VIEWSTATE"]/@value')[0],
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        'ctl00$ContentPlaceHolder1$ctl00$ctl00$skbLogin$DropDownList2': '0',
        'ctl00$ContentPlaceHolder1$ctl00$ctl00$skbLogin$DropDownList3': '0',
        'ctl00$ContentPlaceHolder1$ctl00$ctl00$skbLogin$ibSumbit.x': '37',
        'ctl00$ContentPlaceHolder1$ctl00$ctl00$skbLogin$ibSumbit.y': '14'
    }
    form_data.update(credentials)
    return form_data


def parse_balance(html, session):
    data = {
        'ctl00_ToolkitScriptManager1_HiddenField': '',
        '__EVENTVALIDATION': html.xpath(
            '//input[@id="__EVENTVALIDATION"]/@value')[0],
        '__VIEWSTATE': html.xpath('//input[@id="__VIEWSTATE"]/@value')[0],
        '__EVENTTARGET': ('ctl00$ContentPlaceHolder1$Banner$'
                          'DesktopThreePanes1$ThreePanes$ctl06'),
        '__EVENTARGUMENT': 'P1',
        '__PREVIOUSPAGE': html.xpath('//input[@id="__PREVIOUSPAGE"]/@value')[0]
    }
    r = session.post(balance_url, data=data)
    html = _html.fromstring(r.text)

    accounts = html.xpath(
        '//table[@rules="all"]/tr[position()>1]/td[2]/font/text()[1]')
    currencies = html.xpath(
        '//table[@rules="all"]/tr[position()>1]/td[3]/font/text()')
    amounts = html.xpath(
        '//table[@rules="all"]/tr[position()>1]/td[4]/font/text()')

    regex_account = re.compile('\d+')
    regex_currency = re.compile('[A-Z]{3}')
    regex_amount = re.compile('[0-9,\.]+')

    data = []
    for account, currency, amount in zip(accounts, currencies, amounts):
        try:
            account = regex_account.search(account).group(0)
            currency = regex_currency.search(currency).group(0)
            amount = regex_amount.search(amount).group(0)
        except AttributeError:
            pass
        else:
            data.append((account, currency, amount))

    return data


def logout_data(html, session):
    data = {
        'ctl00_ToolkitScriptManager1_HiddenField': '',
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': html.xpath('//input[@id="__VIEWSTATE"]/@value')[0],
        '__PREVIOUSPAGE': html.xpath(
            '//input[@id="__PREVIOUSPAGE"]/@value')[0],
        '__EVENTVALIDATION': html.xpath(
            '//input[@id="__EVENTVALIDATION"]/@value')[0],
        'ctl00$LoginStatus1$ctl01.x': '19',
        'ctl00$LoginStatus1$ctl01.y': '8'
    }
    session.post(logout_url, data=data)
