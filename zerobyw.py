from common import http_get, write_result

def main() -> None:
    res = http_get('https://raw.githubusercontent.com/zerozzz123456/1/main/url.json')

    url = res.json()['url'].strip().rstrip('/')

    scheme, sep, domain = url.partition('://')
    assert sep == '://'
    assert scheme == 'http' or scheme == 'https'
    assert '/' not in domain

    domain = domain.removeprefix('www.')
    write_result('zerobyw.txt', url, f'Zerobyw {domain}')
