#!/bin/env python
"""
A server that forwards GitHub WebHook POSTs to other destinations based on
rules that map GitHub repositories to a list of forwarding destinations.

This allows an organization to have many internal systems react to GitHub's
post-receive WebHooks and only expose a single service (this app) to the
public-facing internet, potentially decreasing the surface area for an attack.
"""

import json
import requests
import logging
from flask import Flask, request

app = Flask(__name__)
log = app.logger

if not app.debug:
    formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    app.logger.addHandler(console_handler)
    app.logger.setLevel('DEBUG')

with open('./forwarding-rules.json') as forwarding_rules_file:
    forwarding_rules = json.load(forwarding_rules_file)


@app.route('/', methods=['POST'])
def web_hook():
    log.debug('Received POST from {}'.format(request.remote_addr))
    data = json.loads(request.form['payload'])
    data_json = json.dumps(data)

    owner = data['repository']['owner']['name']
    repo = data['repository']['name']
    owner_repo = '{}/{}'.format(owner, repo)

    dests = forwarding_rules.get(owner_repo, [])
    log.info("Forwarding {} hook to these destinations: {}".format(owner_repo, dests))
    for dest in dests:
        requests.post(dest, data={'payload': data_json}, verify=False)

    return "OK"

if __name__ == '__main__':
    app.run()
