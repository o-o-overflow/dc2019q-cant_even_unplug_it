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
    # FYI, the subdomains are:
    #   we-had-started-deploying-here.military-grade.pw
    #   boss-made-us-move-to.such-great-security.pw.military-grade.pw
    # Just had Google temporarly redirect them to my website, they get a certificate and it gets logged.
    page_must_contain('https://crt.sh/?q=%25.military-grade.pw', 'such-great-security.pw')


def step2_archive():
    page_must_contain('https://web.archive.org/web/20190303024447/http://such-great-security.pw/', 'robots')
    page_must_contain('https://web.archive.org/web/20190303024447if_/http://such-great-security.pw/robots.txt', 'secrets')  # text pages are iframe'd
    page_must_contain('https://web.archive.org/web/20190303024447/http://such-great-security.pw/secrets/', 'flag')
    page_must_contain('https://web.archive.org/web/20190303024447/http://such-great-security.pw/secrets/flag.html', 'OOO{the_internet_never_forgets_man}')



if __name__ == "__main__":
    print("[ ] Step 1: Looking up info on crt.sh, the Certificate Transparency public query site...")
    step1_ct()
    print("[ ] Step 2: Looking up the pages on the Internet Archive...")
    step2_archive()
    print("[^] It worked! And with none of the servers active :D")
