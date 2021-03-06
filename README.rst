TW Banker (台灣銀行家)
========================

.. image:: https://badge.fury.io/py/twbanker.svg
    :target: http://badge.fury.io/py/twbanker

Show you the money in your Taiwan banks with a simple command::

    $ twbanker ctbc
    ID card number: ***
    Username: ***
    Password: ***
    TWD     1000.00     000000123456789
    USD      100.00     000000987654321
    -----------------------------------
    TWD     4000.00               TOTAL

Current supported banks

* Chunghwa Post (中華郵政)
* CTBC Bank (中國信託)
* First Bank (第一銀行)
* Shin Kong Bank (新光銀行)
* Standard Chartered (渣打銀行)


Installation
------------
::

    (sudo) pip install twbanker


Usage
-----
::

    $ twbanker --help
    Usage: twbanker [OPTIONS] COMMAND [ARGS]...

      Show you the money in your Taiwan banks.

    Options:
      --help  Show this message and exit.

    Commands:
      chartered  Show you money in Standard Chartered
      ctbc       Show you money in CTBC Bank
      first      Show you money in First Bank
      post       Show you money in Chunghwa Post
      shinkong   Show you money in Shin Kong Bank


How It Works & Disclaimer
-------------------------

TW Banker is a simple web crawler that logs in your bank's web site and parses
out your bank balances. It asks for your login crendentials every time you
execute the command. It does not store any of your login crendentials locally
nor remotely, so using this tool should be pretty safe.

I use this tool personally and I will do my best to make it safe to use.
However, I do not guarantee that the tool is 100% safe. I (the author) and any
future contributors of TW Banker will not account for any lost caused by using
this tool. Please use at your own risk.
