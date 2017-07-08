#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup


class Mantis:

    def __init__(self):
        self.ses = requests.session()

    def login(self, user, password):
        data = [
            ('return', 'index.php'),
            ('username', user),
            ('password', password),
            ('perm_login', 'on'),
        ]

        f = self.ses.post('https://mantis.igna.uy/login.php', data=data)
        return 'password you entered is incorrect.' not in f.text


if __name__ == "__main__":
    m = Mantis()
    s = m.login('administrator', 'root')
    print s
