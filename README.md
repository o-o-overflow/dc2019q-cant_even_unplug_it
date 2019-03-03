## An offline recon challenge, literally

[![Build Status](https://travis-ci.com/o-o-overflow/dc2019q-cant_even_unplug_it.svg?token=6XM5nywRvLrMFwxAsXj3&branch=master)](https://travis-ci.com/o-o-overflow/dc2019q-cant_even_unplug_it)

 1. Use certificate transparency to find subdomains.
 2. Those names hint to the next step: look it up on the Internet Archive. 
 3. The homepage mentions robots being excluded
 4. robots.txt mentions /secrets/flag.html (the directory listing is also indexed, just in case)

I'm keeping the domains registered just in case, but everything is already logged and should stay offline.

The [check script](interaction/check.py) queries crt.sh and archive.org to make sure everything is still there.
