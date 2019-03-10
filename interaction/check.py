#!/usr/bin/env python3

import tempfile
import urllib.request



def page_must_contain(url, needle):
    with urllib.request.urlopen(url) as r:
        content = r.read().decode()
        if needle not in content:
            with tempfile.NamedTemporaryFile('w', suffix='.html', prefix='pagecontent', delete=False) as f:
                f.write(content)
                content_dump_filename = f.name
            raise Exception("Could not find '{}' in page {} -- page content dumped to {}".format(needle, url, content_dump_filename))
    print("[*] Good, '{}' was found on {}".format(needle, url))




def step1_ct():
    # Turns out letsencrypt makes common-names by default, and CNs cannot be more than 64 characters
    # We can only suggest the subdomain as the first step, the full name does not fit :(
    page_must_contain('https://crt.sh/?q=%25.military-grade-secrets.dev', 'even-more-militarygrade.pw')
    page_must_contain('https://crt.sh/?q=%25.even-more-militarygrade.pw', 'forget-me-not.even-more-militarygrade.pw')


def step2_archive():
    page_must_contain('https://web.archive.org/web/20190311064603/https://forget-me-not.even-more-militarygrade.pw/', 'OOO{DAMNATIO_MEMORIAE}')
    # Potentially also http://archive.is/forget-me-not.even-more-militarygrade.pw
    # I'm going to leave it on for some time, so it should also end up in Censys / Shodan / etc.



if __name__ == "__main__":
    print("[ ] Step 1: Looking up info on crt.sh, the Certificate Transparency public query site...")
    step1_ct()
    print("[ ] Step 2: Looking up the pages on the Internet Archive...")
    step2_archive()
    print("[^] It worked!")
