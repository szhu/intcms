# intcms

A lightweight, self-contained CMS for Python 2.4+ and sane people.

_By [@interestinglythere](https://github.com/interestinglythere), in case you didn't figure out from the name._


## What?

**intcms** is content management system (CMS) for small websites. It features a simple templating system centered around filters or 'includes', which allow for transformations of up to a single argument. 


## Why?

1. **It's small.** < 300 SLOC. You can probably edit this stuff in Notepad if you want.
2. **It's easy to learn.** There are pages. There are static files. There are widgets and other types of includes — learn only what you need.
3. **It's manageable** for a single sane non-developer person. You'll only have to work with a few files, and it's all pretty logical.
4. **It's flexible.** Want to change where CMS code resides? Want to change the static files directory? (Spoiler: there is no such special directory.) **intcms** doesn't assume much about your setup. Want to extend the CMS? Want to mess with the internals? The code's right in front of you.
5. **It has virtually no dependencies** beyond UNIX, CGI, and Python. There are lots of web hosts still running Python 2.4 and only basic CGI; **intcms** is for those who'd rather deal with it then* complain.
6. **It doesn't require root access.** **intcms** works within the limitations set by most webhosts. The only configuration required is four lines (found below) inserted in `.htaccess`. It's about as plug-and-play as you can get.

\* That's not a typo. Demand the latest software. Or, if you're on a free webhost, ask very nicely.


## How?

1. Download the files in `cms`.
2. Add this to your root `.htaccess` file:

		RewriteEngine On
		RewriteBase /
		RewriteCond %{REQUEST_FILENAME} !-f
		RewriteRule ^(.*)$ /cms/go.cgi/$1 [QSA,L]

3. Edit `pages/_/page.html` to make your homepage!
4. Then y— wait, that's it? I think that's it.


## The Deets

Coming soon!

## License

I'm not sure yet, so &copy; All rights reserved&hellip; for now. Expect a pretty open license eventually. Contact me if you would like to fork/use for the time being.

## Who?

A guy who goes by [Sean Zhu](http://interestinglythere.com/) has been writing and using predecessors of **intcms** for 4 years. He finally decided to publish the code because of reasons.