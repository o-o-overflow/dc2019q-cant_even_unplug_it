#!/bin/bash -eux
rsync -av --delete this_was_the_website/ root@such-great-security.pw:/var/www/html/
ssh root@such-great-security.pw chmod -R a+rX /var/www/html/
