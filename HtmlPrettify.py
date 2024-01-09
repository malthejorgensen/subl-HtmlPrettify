import re
from html.parser import HTMLParser

from sublime import Region
import sublime_plugin


class Parser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.html_prettified = ''
        self.indent_level = 0
        self.indent_prefix = ''

    def handle_starttag(self, tag, attrs):
        attrs_string = ''
        for key, value in attrs:
            if value:
                attrs_string += ' ' + key + '="' + value + '"'
            else:
                attrs_string += ' ' + key

        tag_str = '<' + tag + attrs_string + '>'
        self.html_prettified += self.indent_prefix + tag_str + '\n'

        # Don't indent self-closing HTML tags
        if tag not in ('img', 'br'):
            self.indent_level += 1
            self.indent_prefix = '  ' * self.indent_level

    def handle_endtag(self, tag):
        self.indent_level -= 1
        self.indent_prefix = '  ' * self.indent_level
        self.html_prettified += self.indent_prefix + '</' + tag + '>' + '\n'

    def handle_data(self, data):
        self.html_prettified += self.indent_prefix + data + '\n'

    def handle_entityref(self, name):
        self.html_prettified += self.indent_prefix + '&' + name + ';' + '\n'

    def handle_charref(self, name):
        self.html_prettified += self.indent_prefix + '&#' + name + ';'


def html_prettify(self, content):
    parser = Parser()
    parser.feed(content)

    return parser.html_prettified


def apply_text_transform(view, edit, region, content, text_transform):
    new_content = text_transform(content)

    view.replace(edit, region, new_content)


class BaseCommand:
    def run(self, edit):
        if self.view.sel()[0].empty() and len(self.view.sel()) == 1:
            # No selection: Transform whole file
            # all_content = self.view.substr(Region(0, self.view.size()))
            # region = all_content
            region = Region(0, self.view.size())

            apply_text_transform(
                self.view,
                edit,
                region,
                self.view.substr(region),
                self.converter_func,
            )
            return

        for region in self.view.sel():
            if region.empty():
                # Empty region
                continue
            else:
                apply_text_transform(
                    self.view,
                    edit,
                    region,
                    self.view.substr(region),
                    self.converter_func,
                )


class HtmlPrettify(BaseCommand, sublime_plugin.TextCommand):
    converter_func = html_prettify
