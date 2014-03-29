# intcms

A lightweight, self-contained CMS for Python 2.6+ and sane people.

## What?

**intcms** is content management system (CMS) for small websites. It’s a lightweight wrapper around the [Jinja2][] templating engine. It supports:

- hierarchal templating
- error pages (can be part of same hierarchy)
- redirects
- quickly add ninja globals and filters
- directory listing

**intcms** is largely file-based and runs on Apache. It is designed for people on small web hosts with big ideas. It probably isn't very efficient unless you set up caching, but should be adequate for personal sites (or you could set up caching).

[jinja2]: http://jinja.pocoo.org/


## Why?

+ **It’s in Python.** For people who like Python.
+ **It’s small,** less than 300 lines of code. It shouldn't be that hard to hack.
+ **It’s easy to learn.** It’s based on Jinja, which is similar to (if not the same as) templating languages you already use.
+ **It’s file-based.** Just use `page.html` for templates, instead of static pages. It plays nicely with Apache, so you can still use `index.html` for static pages.
+ **It’s flexible.** Want to change where CMS code resides? **intcms** doesn't assume much about your setup.
+ **It has just a few dependencies:** Apache, CGI, and Python. Lots of web hosts don't run Node or Ruby on Rails. That doesn't mean you can't have the website you want.
+ **It doesn't require root access.** The only configuration required is a few lines in `.htaccess` (see `intcms.htaccess`).


## How?

### Quick start

1. Download this repo.
2. Create this directory structure in `public_html`:

       + .htaccess    (copy from intcms.htaccess from the repo)
       + _/
         + intcms     (intcms from the repo)
         + templates/ (global templates go here)
         + page.html  (homepage template goes here)


3. Download dependencies `jinja2` and `markupsafe`. No root access? Just place the modules in `intcms`.
4. Add the content in `intcms.htaccess` to your `.htaccess` file.
5. Make your home page in `_/page.html`! (You can also put `page.html` in the web root if you want.)

### Some more fun

- In any directory:
    - add `redirect.{301,302,permanently,temporarily}.txt` to make a redirect
    - add `redirect.{301,302,permanently,temporarily}.wildcard.txt` to make a wildcard redirect
    - manually display an error page anywhere by making a `page.html` with: `{% do status.set(404) %}`
- Want to make the page template publicly hidden? Rename it to `.htpage.html`
- `_/templates/` is for global templates.
    - Want a template for your entire site? Put a `site.html` template there and begin your page templates with `{% extends "site.html" %}`
    - Want directory listings? Make a `directory.html` template in `templates`.

## License

Use **intcms** as you please. Have fun with it, please.

## Who uses **intcms**?

**intcms** is the culmination of [Sean Zhu](http://github.com/interestinglythere)’s work on [interestinglythere.com](http://interestinglythere.com/) over the past 6 years. It also powers [szhu.me](http://szhu.me/). [oratory.berkeley.edu](http://oratory.berkeley.edu/) runs an older version of **intcms**.
