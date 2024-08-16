import re

from httpx import URL, Client, Response

from common import http_get, write_result

def get_domain(client: Client, domain: str) -> Response:
    return client.get(f'https://{domain.replace('-', '--').replace('.', '-')}.translate.goog/?_x_tr_sl=auto&_x_tr_tl=zh-TW', headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })


def main() -> None:
    with open('jmcomic-link.txt') as f:
        link_domain = f.read()

    with Client() as client:
        if (res := get_domain(client, link_domain)).is_redirect:
            subdomain, _, domain = URL(res.headers['Location']).host.partition('.')
            assert domain == 'translate.goog'
            link_domain = subdomain.replace('--', '#').replace('-', '.').replace('#', '-')
            write_result('jmcomic-link.txt', link_domain, f'JM-link {link_domain}')
            assert (res := get_domain(client, link_domain)).is_success

    text = (text := res.text)[(index := text.index('<body>') + 6) : text.index('<script>', index)]
    text = text.replace('&nbsp;', ' ')
    text = re.sub(r'<.+?>', ' ', text)
    domains = re.findall(r'[-\w]+\.[-\w.]+', text)
    assert domains[:4] == ['18comic.vip', '18comic.org', 'jmcomic.me', 'jmcomic1.me']
    end = domains.index('jm365.work')
    assert end > 4
    domains = ','.join(domains[4:end])


    write_result('jmcomic.txt', domains, f'JM {domains}')

main()
