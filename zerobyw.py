import httpx

try:
    res = httpx.get('https://raw.githubusercontent.com/zerozzz123456/1/main/url.json')
    if res.status_code != 200:
        raise Exception(f'HTTP {res.status_code}')

    url = res.json()['url']

    with open('zerobyw.txt', 'w') as f:
        f.write(url)

    with open('.git/COMMIT_EDITMSG', 'w') as f:
        f.write(f'Zerobyw {url}')

except BaseException as e:
    print(f'::error ::{e}')
    exit(1)
