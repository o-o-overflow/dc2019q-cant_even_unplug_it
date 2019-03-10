#!/bin/bash -eux
rsync -av --delete this_was_the_website/ root@forget-me-not.even-more-militarygrade.pw:/var/www/html/
ssh root@forget-me-not.even-more-militarygrade.pw chmod -R a+rX /var/www/html/
