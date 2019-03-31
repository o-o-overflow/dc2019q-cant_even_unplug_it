#!/usr/bin/env python3

import sys
import tempfile
import urllib3
urllib3.disable_warnings()  # Too annoying, and it doesn't really matter here
http = urllib3.PoolManager(retries=10)

def page_must_contain(url, needle):
    r = http.request('GET',url)
    content = r.data.decode('utf-8')
    if needle not in content:
        with tempfile.NamedTemporaryFile('w', suffix='.html', prefix='pagecontent', delete=False) as f:
            f.write(content)
            content_dump_filename = f.name
        raise Exception("Could not find '{}' in page {} -- page content dumped to {}".format(needle, url, content_dump_filename))
    print("[*] Good, '{}' was found on {}".format(needle, url))


def get_exception(url):
    try:
        r = http.request('GET',url)
        assert r.data
        return None   # Possibly: assert
    except urllib3.exceptions.MaxRetryError as e:
        return e.reason
    except urllib3.exceptions.HTTPError as e:
        return e




def step1_ct():
    # Turns out letsencrypt makes common-names by default, and CNs cannot be more than 64 characters
    # We can only suggest the subdomain as the first step, the full name does not fit :(
    page_must_contain('https://crt.sh/?q=%25.military-grade-secrets.dev', 'even-more-militarygrade.pw')
    page_must_contain('https://crt.sh/?q=%25.even-more-militarygrade.pw', 'forget-me-not.even-more-militarygrade.pw')


def step2_archive():
    page_must_contain('https://web.archive.org/web/20190311064603/https://forget-me-not.even-more-militarygrade.pw/', 'OOO{DAMNATIO_MEMORIAE}')
    # Potentially also http://archive.is/forget-me-not.even-more-militarygrade.pw
    # I'm going to leave it on up to the competition and leave the DNS records on, so it should also end up in Censys / Shodan / Google / ...


def check_down_with_dns():
    # Self-check first
    e = get_exception("https://down.jacopo.cc"); assert isinstance(e, urllib3.exceptions.ConnectTimeoutError), \
        "SELF-CHECK ERROR: Failed to check down.jacopo.cc is in fact down (I wanted ConnectTimeoutError, got {})".format(e)
    e = get_exception("https://nonexistent.jacopo.cc"); assert isinstance(e, urllib3.exceptions.NewConnectionError), \
        "SELF-CHECK ERROR: Failed to check nonexisting DNS (I wanted NewConnectionError, got {})".format(e)  # Reliable DNS vs. other errors?
    # Then check the real sites
    e = get_exception("https://forget-me-not.even-more-militarygrade.pw")
    if e is None:
        print("WARN: The site is still up! Remember to turn it off before the game!")
        sys.stderr.write("\n\n\n **************** WARNING **********\n\n  The site is still up! Remember to turn it off before the game!\n\n\n\n\n")
    else:
        assert isinstance(e, urllib3.exceptions.ConnectTimeoutError), \
                "DNS down or something? I was expecting unreachable/not-available, got {} instead".format(e)
        print("Site is already down, good if quals are tomorrow :D")



if __name__ == "__main__":
    print("[ ] Step 1: Looking up info on crt.sh, the Certificate Transparency public query site...")
    step1_ct()
    print("[ ] Step 2: Looking up the pages on the Internet Archive...")
    step2_archive()
    print("[^] CT + Wayback machine search worked, good.")

    check_down_with_dns()
