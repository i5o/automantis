#!/usr/bin/env python

import re
import requests
from bs4 import BeautifulSoup

regex_result = u'<a class="btn btn-primary btn-white btn-round " href="(.*?)">'


class Mantis:

    def __init__(self, server):
        self.ses = requests.session()
        self.server = server

    def login(self, user, password):
        data = [
            ('return', 'index.php'),
            ('username', user),
            ('password', password),
            ('perm_login', 'on'),
        ]

        f = self.ses.post('%s/login.php' % self.server, data=data)
        return 'password you entered is incorrect.' not in f.text

    def logout(self):
        self.ses.get('%s/logout_page.php' % self.server)

    def report_bug(self, summary, description, category_id="1",
                   steps_to_reproduce="", additional_info="", tags=[]):
        web_data = self.ses.get(
            '%s/bug_report_page.php' %
            self.server)
        bug_form = BeautifulSoup(
            web_data.content,
            "lxml").find_all('form')[1]  # 2
        inputs = bug_form.find_all('input')

        post_keys = {}

        for input_html in inputs:
            if input_html.has_attr('value') and input_html.has_attr('name'):
                post_keys[input_html['name']] = input_html['value']

        post_keys["summary"] = summary
        post_keys["description"] = description
        post_keys["category_id"] = category_id
        if steps_to_reproduce:
            post_keys["steps_to_reproduce"] = steps_to_reproduce

        if additional_info:
            post_keys["additional_info"] = additional_info

        if tags:
            post_keys["tag_string"] = ",".join(tags)

        result = self.ses.post(
            '%s/bug_report.php' %
            self.server, data=post_keys)
        link = re.findall(regex_result, result.content)[0]
        return "%s/%s" % (self.server, link)


if __name__ == "__main__":
    m = Mantis('http://mantis.igna.uy')
    m.login('administrator', 'broken')
    link = m.report_bug("Hello", "world")
    print "reported %s" % link
    m.logout()
