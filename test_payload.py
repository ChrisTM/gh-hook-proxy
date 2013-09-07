#!/bin/env python
"""
A tool for testing ``gh-hook-proxy`` by POSTing fake GitHub hook payloads and
printing the response.
"""

import argparse
import requests
import json


def craft_payload_data(repo_owner='ChrisTM', repo_name='gh-hook-proxy'):
    """
    Return a dictionary with sample GitHub hook payload data for the repository
    specified by ``repo_owner`` and ``repo_name``.
    """
    repo_owner_email = '{}@example.com'.format(repo_owner)
    user_obj = {
        'name': repo_owner,
        'email': repo_owner_email
    }

    # Payload modelled after the template shown here:
    # https://help.github.com/articles/post-receive-hooks#the-payload
    return {
        'before': '20ceddf69021a0b1bac73587df73f726e87a5945',
        'after': '871aa44e212e34f7a80853687e4d104f1f9d54ea',
        'ref': "refs/heads/master",
        # Jenkins' GitHub plugin expects ``pusher``. See https://github.com/jenkinsci/github-plugin/blob/0604bacbf51cf3af7400b4956ecf3a57a6024d29/src/main/java/com/cloudbees/jenkins/GitHubWebHook.java#L162
        'pusher': user_obj,
        'commits': [
            #{
            #    'id': '196d59506634023e47f581bc3b2d4a462ec46466',
            #    'message': 'This is a commit message.',
            #    'timestamp': '2013-08-02T11:13:17-07:00',
            #    'url': '',
            #    'added': [],
            #    'removed': [],
            #    'modified': [],
            #    'author': user_obj,
            #},
        ],
        'repository': {
            'name': repo_name,
            'url': 'https://github.com/{}/{}'.format(repo_owner, repo_name),
            'description': '',
            'homepage': '',
            'watchers': 0,
            'forks': 0,
            'private': False,
            'owner': user_obj,
        },
    }


def post_hook(url, payload_data):
    """
    POST a GitHub hook request to ``url`` containing the payload data in
    ``payload_data`` and return a ``requests`` response object.
    """
    payload_json = json.dumps(payload_data)
    return requests.post(url, data={'payload': payload_json}, verify=False)


def create_parser():
    parser = argparse.ArgumentParser(
        description='Send a fake GitHub hook request and print the response.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '--repo-owner',
        default='ChrisTM',
        help='Name of repo owner to use in request.'
    )
    parser.add_argument(
        '--repo-name',
        default='gh-hook-proxy',
        help='Name of repo to use in request.'
    )
    parser.add_argument(
        '--url',
        default='http://127.0.0.1:5000/',
        help='URL to POST the request to'
    )

    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()

    payload_data = craft_payload_data(
        repo_owner=args.repo_owner, repo_name=args.repo_name)

    response = post_hook(args.url, payload_data)
    text = response.text.encode('utf-8')
    print text
