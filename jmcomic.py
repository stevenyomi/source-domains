import re
from os import getenv

from httpx import URL, Client

from common import extract_location, get_domain, write_result


def retry_get(client: Client, url: str):
    attempts = 5
    while True:
        try:
            if (res := client.get(url)).status_code == 430:
                raise Exception(f'HTTP {res.status_code}')
            return res
        except Exception:
            if (attempts := attempts - 1) == 0:
                raise


def main() -> None:
    with open('jmcomic-link.txt') as f:
        link_domain = f.read().partition('||')[0]

    with Client() as client:
        while (res := get_domain(client, link_domain)).is_redirect:
            link_domain = extract_location(res)
        if res.is_success:
            write_result('jmcomic-link.txt', f'{link_domain}||g', f'JM-link(g) {link_domain}')
        else:
            assert (proxy := getenv('JM_PROXY'))
            while (res := retry_get(client, f'https://{proxy}/https://{link_domain}/')).is_redirect:
                link_domain = URL(res.headers['Location']).host
            if res.is_success:
                write_result('jmcomic-link.txt', f'{link_domain}||p', f'JM-link(p) {link_domain}')
            else:
                raise Exception(f'HTTP {res.status_code}')

    text = (text := res.text)[(index := text.index('<div')) : text.index('<script>', index)]
    text = text.replace('&nbsp;', ' ')
    text = re.sub(r'<.+?>', ' ', text)
    domains = re.findall(r'[-\w]+\.[-\w.]+', text)
    # TODO: new fixed domains + possible redirection
    assert domains[:4] == ['18comic.vip', '18comic.org', 'jmcomic.me', 'jmcomic1.me']
    end = domains.index('jm365.work')
    assert end > 4
    domains = ','.join(map(str.lower, domains[4:end]))


    write_result('jmcomic.txt', domains, f'JM {domains}')

main()
