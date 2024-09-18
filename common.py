from subprocess import run
from sys import stderr, stdout

from httpx import URL, Client, Response, get


def http_get(url: str, *, headers=None):
    if (res := get(url, headers=headers)).status_code != 200:
        raise Exception(f"HTTP {res.status_code}")
    return res


def http_retry_get(url: str):
    from tenacity import retry, stop_after_attempt

    @retry(stop=stop_after_attempt(3))
    def make_request(client: Client, url: str):
        res = client.get(url)
        if res.status_code >= 500:
            raise Exception(f"HTTP {res.status_code}")
        return res

    with Client() as client:
        res = make_request(client, url)

    if res.status_code != 200:
        raise Exception(f"HTTP {res.status_code}")
    return res


def get_domain(client: Client, domain: str) -> Response:
    subdomain = domain.replace("-", "--").replace(".", "-")
    return client.get(
        f"https://{subdomain}.translate.goog/?_x_tr_sl=auto&_x_tr_tl=zh-TW",
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                " Chrome/120.0.0.0 Safari/537.36"
            )
        },
    )


def extract_location(res: Response) -> str:
    subdomain, _, domain = URL(res.headers["Location"]).host.partition(".")
    assert domain == "translate.goog"
    return subdomain.replace("--", "#").replace("-", ".").replace("#", "-")


def write_result(filename: str, content: str, commit_message: str) -> None:
    with open(filename, "w") as f:
        f.write(content)

    if run(("git", "status", "--porcelain"), check=True, capture_output=True).stdout:
        run(("git", "add", filename), check=True, stdout=stdout, stderr=stderr)
        run(("git", "commit", "-m", commit_message), check=True, stdout=stdout, stderr=stderr)
