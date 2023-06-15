import httpx

try:
    res = httpx.get('https://raw.githubusercontent.com/zerozzz123456/1/main/url.json')
    if res.status_code != 200:
        raise Exception(f'HTTP {res.status_code}')

    url = res.json()['url'].strip().rstrip('/')

    scheme, sep, domain = url.partition('://')
    assert sep == '://'
    assert scheme == 'http' or scheme == 'https'
    assert '/' not in domain

    with open('zerobyw.txt', 'w') as f:
        f.write(url)

    domain = domain.removeprefix('www.')
    with open('.git/COMMIT_EDITMSG', 'w') as f:
        f.write(f'Zerobyw {domain}')

except BaseException as e:
    print(f'::error ::{e}')
    exit(1)
