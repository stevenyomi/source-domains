from common import http_get, write_result

def main() -> None:
    res = http_get('https://raw.githubusercontent.com/zerozzz123456/1/main/appconfig.json')

    url = 'http:' + res.json()['websitedomain'].strip().rstrip('/')

    scheme, sep, domain = url.partition('://')
    assert sep == '://'
    assert scheme == 'http'
    assert '/' not in domain

    domain = domain.removeprefix('www.')
    write_result('zerobyw.txt', url, f'Zerobyw {domain}')
