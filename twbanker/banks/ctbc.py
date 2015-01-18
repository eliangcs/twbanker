name = 'CTBC Bank'

form_url = 'https://www.ctbcbank.com/CTCBPortalWeb/appmanager/ebank/rb'

login_url = ('https://www.ctbcbank.com/CTCBPortalWeb/appmanager/ebank/rb?'
             'loginservice.faces')

balance_url = ('https://www.ctbcbank.com/CTCBPortalWeb/appmanager/ebank/rb?'
               '_nfpb=true&_pageLabel=TW_RB_TX_ebank_049341')

logout_url = ('https://www.ctbcbank.com/CTCBPortalWeb/appmanager/ebank/rb?'
              '_nfpb=true&_pageLabel=TW_RB_TX_HiddenPagecomm_098291&'
              'doUserLogout=immediately')

credentials = (
    ('ID card number', 'id'),
    ('Username', 'userid'),
    ('Password', 'passwd'),
)


def get_form_data(html, credentials):
    token = html.xpath(
        '//form[@name="loginform"]/input[@name="token"]/@value')[0]
    form_data = {
        'token': token,
        'doUserLogin': 'immediately',
        'ctcb_select_test:default_select_value': '',
        'ref_pageLabel': '',
        'identityTokenId': 'undefined',
        'identityUserId': 'undefined',
        'identityReqSystem': 'undefined'
    }
    form_data.update(credentials)
    return form_data


def parse_balance(html):
    twd_accounts = html.xpath(
        '//tbody[contains(@id, ":twddata")]//select/option[1]/@value')
    twd_balances = html.xpath(
        '//tbody[contains(@id, ":twddata")]/tr/td[2]/text()')[:-1]

    # Foreign currencies
    fc_accounts = html.xpath(
        '//tbody[contains(@id, ":fcdata")]//select/option[1]/@value')
    fc_currencies = html.xpath(
        '//tbody[contains(@id, ":fcdata")]/tr/td[2]/text()')[:-1]
    fc_balances = html.xpath(
        '//tbody[contains(@id, ":fcdata")]/tr/td[3]/text()')[:-1]

    data = []
    for account, balance in zip(twd_accounts, twd_balances):
        data.append((account, 'TWD', balance))
    for account, balance, currency in zip(fc_accounts, fc_balances,
                                          fc_currencies):
        data.append((account, currency[:3], balance))
    return data
