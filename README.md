HtmlPrettify
===========
**HtmlPrettify** is a Sublime Text package that prettifies HTML.

It adds the command _HtmlPrettify: Prettify HTML_ to the Command Palette.


_WARNING: This is an alpha. It may remove parts of your HTML,
or add newlines where they weren't intended. Backup your files before using it._


How does it work?
-----------------
It uses the Python 3 built-in `html.parser.HTMLParser` parse and beautify the HTML.
