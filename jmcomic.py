import re

from httpx import Client

from common import extract_location, get_domain, write_result


def main() -> None:
    with open('jmcomic-link.txt') as f:
        link_domain = f.read()

    with Client() as client:
        if (res := get_domain(client, link_domain)).is_redirect:
            link_domain = extract_location(res)
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
