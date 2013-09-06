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
    # Payload modelled after the template shown here:
    # https://help.github.com/articles/post-receive-hooks#the-payload
    return {
        'before': '20ceddf69021a0b1bac73587df73f726e87a5945',
        'after': '871aa44e212e34f7a80853687e4d104f1f9d54ea',
        'ref': "refs/heads/master",
        'commits': [
            #{
            #    'id': commit.id,
            #    'message': commit.message,
            #    'timestamp': commit.committed_date.xmlschema,
            #    'url': commit_url,
            #    'added': array_of_added_paths,
            #    'removed': array_of_removed_paths,
            #    'modified': array_of_modified_paths,
            #    'author': {
            #        'name': commit.author.name,
            #        'email': commit.author.email
            #    }
            #}
        ],
        'repository': {
            'name': repo_name,
            'url': 'https://github.com/{}/{}'.format(repo_owner, repo_name),
            'description': '',
            'homepage': '',
            'watchers': 0,
            'forks': 0,
            'private': False,
            'owner': {
                'name': repo_owner,
                'email': '{}@example.com'.format(repo_owner)
            }
        }
    }


def post_hook(url, payload_data):
    """
    POST a GitHub hook request to ``url`` containing the payload data in
    ``payload_data`` and return a ``requests`` response object.
    """
    return requests.post(url, data={'payload': json.dumps(payload_data)})


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
    r = post_hook(args.url, payload_data)
    print r.text
