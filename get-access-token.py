#!/usr/bin/env python
# Copyright 2007-2018 The Python-Twitter Developers <- took their oauth logic
from __future__ import print_function
from requests_oauthlib import OAuth1Session
import webbrowser
import twitter
import sys

if sys.version_info.major < 3:
    input = raw_input

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'
SIGNIN_URL = 'https://api.twitter.com/oauth/authenticate'


def get_access_token(consumer_key, consumer_secret):
    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret, callback_uri='oob')

    print('\nRequesting temp token from Twitter...\n')

    resp = oauth_client.fetch_request_token(REQUEST_TOKEN_URL)

    url = oauth_client.authorization_url(AUTHORIZATION_URL)

    print('I will try to start a browser to visit the following Twitter page '
          'if a browser will not start, copy the URL to your browser '
          'and retrieve the pincode to be used '
          'in the next step to obtaining an Authentication Token: \n'
          '\n\t{0}'.format(url))

    webbrowser.open(url)
    pincode = input('\nEnter your pincode: ')

    print('\nGenerating and signing request for an access token...\n')

    oauth_client = OAuth1Session(consumer_key, client_secret=consumer_secret,
                                 resource_owner_key=resp.get('oauth_token'),
                                 resource_owner_secret=resp.get('oauth_token_secret'),
                                 verifier=pincode)
    try:
        resp = oauth_client.fetch_access_token(ACCESS_TOKEN_URL)
    except ValueError as e:
        raise 'Invalid response from Twitter requesting temp token: {0}'.format(e)
    unblock_all(consumer_key, consumer_secret, resp.get('oauth_token'), resp.get('oauth_token_secret'))

def unblock_all(consumer_key, consumer_secret, access_token_key, access_token_secret):
    api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)
    for blocked_id in api.GetBlocksIDs():
        print(f'Unblocking userid: {blocked_id}')
        api.DestroyBlock(user_id=blocked_id)

def main():
    consumer_key = input('Enter your consumer key: ')
    consumer_secret = input('Enter your consumer secret: ')
    get_access_token(consumer_key, consumer_secret)

if __name__ == "__main__":
    main()
