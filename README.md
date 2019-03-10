## An offline recon challenge, literally

[![Build Status](https://travis-ci.com/o-o-overflow/dc2019q-cant_even_unplug_it.svg?token=6XM5nywRvLrMFwxAsXj3&branch=master)](https://travis-ci.com/o-o-overflow/dc2019q-cant_even_unplug_it)

 1. Use certificate transparency to find subdomains.
 2. Those names hint to the homepage. Can be found on the Internet Archive (Censys, etc.)
 3. That's it, I changed my mind on robots.txt stuff.

I'm keeping the domains registered just in case, but everything is already logged and should stay offline.

The [check script](interaction/check.py) queries crt.sh and archive.org to make sure everything is still there.
