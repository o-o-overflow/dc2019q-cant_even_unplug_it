#!/usr/bin/env python3

import sys
import tempfile
import urllib.request
import urllib.error
from errno import ENETUNREACH, ENOENT, EADDRNOTAVAIL  # This is kinda wrong


def page_must_contain(url, needle):
    with urllib.request.urlopen(url) as r:
        content = r.read().decode()
        if needle not in content:
            with tempfile.NamedTemporaryFile('w', suffix='.html', prefix='pagecontent', delete=False) as f:
                f.write(content)
                content_dump_filename = f.name
            raise Exception("Could not find '{}' in page {} -- page content dumped to {}".format(needle, url, content_dump_filename))
    print("[*] Good, '{}' was found on {}".format(needle, url))


def get_exception(url):
    try:
        with urllib.request.urlopen(url) as r:
            r.read()
            return None   # Possibly: assert
    except urllib.error.URLError as e:
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
    e = get_exception("https://down.jacopo.cc"); assert e.reason.errno in (ENETUNREACH,EADDRNOTAVAIL), "SELF-CHECK ERROR: Failed to check down.jacopo.cc is in fact down (got errno != ENETUNREACH, {})".format(e)
    e = get_exception("https://nonexistent.jacopo.cc"); assert e.reason.errno == -ENOENT, "SELF-CHECK ERROR: Failed to check nonexisting DNS (got errno != -ENOENT, {})".format(e)
    # Then check the real sites
    e = get_exception("https://forget-me-not.even-more-militarygrade.pw")
    if e is None:
        print("WARN: The site is still up! Remember to turn it off before the game!")
        sys.stderr.write("\n\n\n **************** WARNING **********\n\n  The site is still up! Remember to turn it off before the game!\n\n\n\n\n")
    else:
        assert e.reason.errno in (ENETUNREACH,EADDRNOTAVAIL), "DNS down or something? I was expecting unreachable/not-available, got {} instead".format(e)
        print("Site is already down, good if quals are tomorrow :D")



if __name__ == "__main__":
    print("[ ] Step 1: Looking up info on crt.sh, the Certificate Transparency public query site...")
    step1_ct()
    print("[ ] Step 2: Looking up the pages on the Internet Archive...")
    step2_archive()
    print("[^] CT + Wayback machine search worked, good.")

    check_down_with_dns()
