import re

from Crypto.Cipher import DES3


name = 'Chunghwa Post'

form_url = 'https://ipost.post.gov.tw/web/CSController'

login_url = 'https://ipost.post.gov.tw/web/CSController'

balance_url = 'https://ipost.post.gov.tw/web/CSController?cmd=CUR1002_1'

logout_url = 'https://ipost.post.gov.tw/web/CSController?cmd=POS0000_5'

credentials = (
    ('Account number (14 digits)', 'USERID'),
    ('Username', 'USERCODE'),
    ('Password', 'PWD'),
)


def get_form_data(html, credentials):
    form_data = {
        'cmd': 'POS0000_2',
        'chgUserIdFalg': '0',
        'isPWDNum': '0',
        'oldUSERTYPE': '1',
        'USERTYPE': '1'
    }
    form_data.update(credentials)

    random_key = 'C9CA5CE988706FC1D2A4E0B350B5A11B0107DB02DBF656ED'
    random_key_encrypted = (
        '3ffc24d945fc680cf0ec04aa7b141d8d4590d48a621b3dd0cfc5967ff8bc4c3dcfa4f'
        'ecaebe58351d5961626f9636eeae7f07ba082e1fc97d9efff96787da5845cdd277245'
        'bda988f4a2e9de2cc0ae5eb4afea3af19213839a1c2fbfc22d8056a07a45154288968'
        '3c5287c529b9f6193203527948091bf5765a85d0a30daf58f')

    des_key = random_key.decode('hex')
    des = DES3.new(des_key, DES3.MODE_ECB, '\0\0\0\0\0\0\0\0')

    pwd_padded = _pad_to_8x(form_data['PWD'])
    usercode_padded = _pad_to_8x(form_data['USERCODE'])

    pwd_encrypted = des.encrypt(pwd_padded).encode('hex').upper()
    usercode_encrypted = des.encrypt(usercode_padded).encode('hex').upper()

    form_data.update({
        'ePin': pwd_encrypted,
        'eKey': random_key_encrypted,
        'usercode_ePin': usercode_encrypted,
        'usercode_eKey': random_key_encrypted,
        'PWD': '*' * len(form_data['PWD'])
    })
    return form_data


def parse_balance(html):
    accounts = html.xpath(
        '//table[@class="Context_tb"]/tr[1]/td[2]/script/text()')
    amounts = html.xpath(
        '//table[@class="Context_tb"]/tr[3]/td[2]/script/text()')

    regex_account = re.compile("^.*'(\d+)'.*$")
    regex_amount = re.compile("^.*'([0-9,\.]+)'.*")

    data = []
    for account, amount in zip(accounts, amounts):
        m1 = regex_account.match(account)
        m2 = regex_amount.match(amount)
        if m1 and m2:
            data.append((m1.group(1), 'TWD', m2.group(1)))
    return data


def _pad_to_8x(s):
    num_chars_to_pad = (8 - len(s) % 8) % 8
    return s + ('\0' * num_chars_to_pad)
