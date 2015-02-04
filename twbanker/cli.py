import click
import importlib
import locale
import os
import requests

from getpass import getpass
from lxml import html


BANKS_DIR = os.path.join(os.path.dirname(__file__), 'banks')

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


def get_exchange_rate(currency):
    r = requests.get('http://finance.yahoo.com/d/quotes.csv?'
                     'e=.csv&f=sl1d1t1&s=%sTWD=X' % currency)
    return float(r.content.split(',')[1])


def generate_bank_command(bank):
    @click.command(help='Show you money in %s' % bank.name)
    def cli():
        user_agent = getattr(bank, 'user_agent', 'Mozilla/5.0')

        s = requests.Session()
        s.headers.update({
            'User-Agent': user_agent
        })
        r = s.get(bank.form_url)
        if r.status_code != 200:
            click.echo('Failed to get login form (%d)' % r.status_code)
            return

        credentials = {}
        for name, codename in bank.credentials:
            credentials[codename] = getpass('%s: ' % name)

        tree = html.fromstring(r.text)
        form_data = bank.get_form_data(tree, credentials, s)

        r = s.post(bank.login_url, data=form_data)
        if r.status_code != 200:
            click.echo('Failed to log in (%d)' % r.status_code)
            return

        try:
            r = s.get(bank.balance_url)
            tree = html.fromstring(r.text)
            total = 0
            for account, currency, amount in bank.parse_balance(tree, s):
                if isinstance(amount, basestring):
                    amount = locale.atof(amount)
                line = '%3s %13.2f %20s' % (currency, amount, account)
                click.echo(line)

                if currency == 'TWD':
                    rate = 1.0
                else:
                    rate = get_exchange_rate(currency)

                total += rate * amount

            click.echo('--------------------------------------')
            click.echo('TWD %13.2f %20s' % (total, 'TOTAL'))

        finally:
            logout_method = getattr(bank, 'logout_method', 'get')
            logout = getattr(s, logout_method)

            logout_data = getattr(bank, 'logout_data', None)
            if callable(logout_data):
                logout_data = logout_data(tree, s)

            r = logout(bank.logout_url, data=logout_data)
            if r.status_code >= 400:
                click.echo('Logout error (%d)' % r.status_code)

    return cli


class Cli(click.MultiCommand):

    def list_commands(self, ctx):
        cmds = []
        for filename in os.listdir(BANKS_DIR):
            if filename.endswith('.py') and not filename.startswith('_'):
                cmds.append(filename[:-3])
        return sorted(cmds)

    def get_command(self, ctx, name):
        try:
            bank = importlib.import_module('twbanker.banks.' + name)
        except ImportError:
            # No such command
            return None
        return generate_bank_command(bank)


@click.group(cls=Cli, help='Show you the money in your Taiwan banks.')
def main():
    pass


if __name__ == '__main__':
    main()
