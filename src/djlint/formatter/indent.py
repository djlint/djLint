
from .parser import HTMLParser
import re
from ..settings import Config


def indent_html(rawcode: str, config: Config):

<<<<<<< HEAD
    elements = []
    class MyHTMLParser(HTMLParser):

        def handle_starttag(self, tag, attrs, tag_type):
            elements.append({"location": "START", "type":tag_type, "tag":tag, "attrs": attrs})
            #print("Encountered a start tag:", tag, " with attrs: ", attrs, " type: ", tag_type)

        def handle_endtag(self, tag, tag_type):
            elements.append({"location": "END", "type":tag_type, "tag":tag})
            #print("Encountered an end tag :", tag, " type: ", tag_type)

        def handle_data(self, data):
            elements.append({"data":data})
            #print("Encountered some data  :", data)

        def handle_comment(self, data, tag_type):
            elements.append({"comment": data, "type":tag_type})


    #print(data)



=======
>>>>>>> 5b6a65a (moved format code into class override)
    ## pop front mater
    rawcode = rawcode.strip()


    front_matter = re.search(r'^---[\s\S]+?---\S*', rawcode)

    if front_matter:
        front_matter = front_matter.group()
        rawcode = rawcode.replace(front_matter,"")

        front_matter = front_matter.strip() + "\n"
    else:
        front_matter = ""

<<<<<<< HEAD

        return bool(re.search(r"[ ]*$", html, re.M))
>>>>>>> 86e2c8b (formatted tests)

    elements = []



    class MyHTMLParser(HTMLParser):
        def __init__(self, config):
            def get_tag_style(style):
                return dict(
                    chain(
                        *map(
                            dict.items,
                            [
                                {y: x["style"].get(style) for y in x["selectorText"].split(",")}
                                for x in list(
                                    filter(lambda x: x["style"].get(style) is not None, html_styles)
                                )
                            ],
                        )
                    )
                )
            super(MyHTMLParser, self).__init__()
            self.output = ""
            self.config = config
            self.indent_html_tags = ["div", "p", "dd"]
            self.ignored_html_tags = ["pre", "code", "textarea", "script"]
            self.inline_blocks = [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
                "a",
                "span",
                "small"
            ]

            self.css_display = dict(**get_tag_style('display'),**{
                  "button": "inline-block",
                  "template": "inline",
                  "source": "block",
                  "track": "block",
                  "script": "block",
                  "param": "block",
                  "details": "block",
                  "summary": "block",
                  "dialog": "block",
                  "meter": "inline-block",
                  "progress": "inline-block",
                  "object": "inline-block",
                  "video": "inline-block",
                  "audio": "inline-block",
                  "select": "inline-block",
                  "option": "block",
                  "optgroup": "block"
                })
            self.css_default_display = "inline"
            self.css_whitespace = get_tag_style('whitespace')
            self.css.default_whitespace = 'normal'

            self.indent_temp_tags = ["if"]
            self.indent_block = False
            self.current_block = "tag"

            self.indent = self.config.indent
            self.level = 0
            self.ignored_level = 0
            self.inline_level = 0
            self.is_inline = False

            self.line_length= 0

        def handle_starttag(self, tag, attrs):

            if tag in html_tag_names:
                tag = tag.lower()
            #print("opening: ", tag)


            attributes = []

            #for attribute in attrs:

            if attrs:
                attribs = " " + (" ").join(
                    [x[0].lower() + ('="' + x[1] + '"' if x[1] else "") for x in attrs]
                )

            html_closing = " />" if tag in html_void_elements else ">"
            html_tag = f"<{tag}{attribs}{html_closing}"

            indent = self.indent * self.level

            if tag in self.ignored_html_tags:
                # print("ignored html tags")
                if self.ignored_level == 0 and breakbefore(self.output):
                    self.output += indent
                elif self.ignored_level == 0 and not breakbefore(self.output):
                    self.output += "\n" + indent
                self.output += html_tag
                if tag not in html_void_elements:
                    self.ignored_level += 1
                    self.current_block = "tag"

            elif tag in self.inline_blocks:
                # print("inline blocks")
                if self.inline_level == 0 and breakbefore(self.output):
                    self.output += self.indent * self.level

                if (
                    self.inline_level == 0
                    and not breakbefore(self.output)
                    and self.current_block == "tag"
                ):
                    self.output += "\n" + indent

                if tag not in html_void_elements:
                    self.inline_level += 1
                self.output += html_tag

                if tag not in html_void_elements:
                    self.current_block = "tag"
            else:
                # print("else")
                # if tag in self.indent_html_tags:
                self.output = self.output.rstrip()
                if self.output and self.output[-1] != "\n":
                    self.output = self.output + "\n"

                self.output += indent

                self.output += html_tag + "\n"
                if tag not in html_void_elements:
                    self.level += 1
                    self.current_block = "tag"

            # else:
            #     self.output += html_tag

        def handle_tempstatestarttag(self, tag, attrs):
            attribs = " " + (" ").join(attrs) + "" if attrs else ""
            if tag in self.indent_temp_tags:
                self.output += (
                    (self.indent * self.level) + "{% " + tag + attribs + " %}\n"
                )
                self.level += 1

        def handle_endtag(self, tag):
            if tag in html_tag_names:
                tag = tag.lower()

            if tag in self.ignored_html_tags:
                self.output += "</" + tag + ">"
                self.ignored_level -= 1
                self.current_block = "tag"

            elif tag in self.inline_blocks:
                self.inline_level -= 1
                self.output += "</" + tag + ">"
                self.current_block = "tag"
            elif tag not in html_void_elements:
                self.output = self.output.rstrip()
                if self.output != "":
                    self.output = self.output + "\n"

                # print("end")
                self.level -= 1
                self.output += (self.indent * self.level) + "</" + tag + ">\n"
                self.current_block = "tag"

        def handle_tempstateendtag(self, tag, attrs):
            attribs = " " + (" ").join(attrs) + "" if attrs else ""
            if tag in self.indent_temp_tags:
                self.level -= 1
                self.output += (self.indent * self.level) + "{% end" + tag + " %}\n"

        def handle_data(self, data):
            if self.ignored_level > 0 or self.inline_level > 0 and data.strip() != "":
                self.output += data
                self.current_block = "text"
            elif data.strip() != "":

                if breakbefore(self.output):
                    self.output += self.indent * self.level
                self.output += re.sub(r"\s+$", " ", data.lstrip(), re.M)
                self.current_block = "text"

        def handle_comment(self, data):
            if breakbefore(self.output):
                self.output += self.indent * self.level
            elif (
                self.ignored_level == 0
                and self.inline_level == 0
                and not breakbefore(self.output)
            ):
                self.output += "\n" + (self.indent * self.level)
            self.output += "<!--" + data + "-->"

        def close(self):
            super(MyHTMLParser, self).close()
            return self.output

    p = MyHTMLParser(config)
    p.feed(rawcode)
    output = p.close()
=======
    p = MyHTMLParser()
    p.feed(rawcode)
    p.close()

=======
>>>>>>> 5b6a65a (moved format code into class override)


    def breakbefore(html):

        return bool(re.search(r"\n[ \t]*$",html, re.M))

    def spacebefore(html):
        return bool(re.search(r"[ ]*$",html, re.M))



    elements = []

    class MyHTMLParser(HTMLParser):
        def __init__(self):
            super(MyHTMLParser,self).__init__()
            self.output = ""
            #self.indent_html_tags = ["div", "p", "dd"]
            self.ignored_html_tags = ["pre","code", 'textarea', 'script']
            self.inline_blocks = ["h1","h2","h3","h4","h5",'h6', "a", "span",  "small"]
            self.self_closing_tags = ["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "para", "source", "track" "wbr", "command", "keygen", "menuitem"]
            self.indent_temp_tags = ["if"]
            self.indent_block = False
            self.current_block = "tag"

            self.indent = config.indent
            self.level = 0
            self.ignored_level = 0
            self.inline_level = 0
            self.is_inline = False

        def handle_starttag(self, tag, attrs):
            tag = tag.lower()
            # print("opening: ", tag)
            # print(attrs)
            attribs = ""
            if attrs:
                attribs = " " + (" ").join([x[0].lower() + ("=\"" + x[1] + "\"" if x[1] else "") for x in attrs])

            html_closing = " />" if tag in self.self_closing_tags else ">"

            html_tag = f"<{tag}{attribs}{html_closing}"

            if tag in self.ignored_html_tags:
                # print("ignored html tags")
                if self.ignored_level == 0 and breakbefore(self.output):
                    self.output += (self.indent * self.level)
                elif self.ignored_level == 0 and not breakbefore(self.output):
                    self.output += "\n" + (self.indent * self.level)
                self.output += html_tag
                if tag not in self.self_closing_tags:
                    self.ignored_level += 1
                    self.current_block = "tag"

            elif tag in self.inline_blocks:
                # print("inline blocks")
                if self.inline_level == 0 and breakbefore(self.output):
                    self.output += (self.indent * self.level)

                if self.inline_level == 0 and not breakbefore(self.output) and self.current_block=="tag":
                    self.output += "\n" + (self.indent * self.level)

                if tag not in self.self_closing_tags:
                    self.inline_level += 1
                self.output += html_tag

                if tag not in self.self_closing_tags:
                    self.current_block = "tag"

            else:
                # print("else")
                #if tag in self.indent_html_tags:
                self.output = self.output.rstrip()
                if self.output and self.output[-1] != "\n":
                    self.output = self.output + "\n"

                self.output += (self.indent * self.level)

                self.output += html_tag + "\n"
                if tag not in self.self_closing_tags:
                    self.level += 1
                    self.current_block = "tag"


            # else:
            #     self.output += html_tag

        def handle_tempstatestarttag(self, tag, attrs):
            attribs = (" " + (" ").join(attrs) + "" if attrs else "")
            if tag in self.indent_temp_tags:
                self.output += (self.indent * self.level) + "{% " + tag + attribs +" %}\n"
                self.level += 1

        def handle_endtag(self, tag):
            tag = tag.lower()
            if tag in self.ignored_html_tags:
                self.output += "</" + tag + ">"
                self.ignored_level -= 1
                self.current_block = "tag"

            elif tag in self.inline_blocks:
                self.inline_level -= 1
                self.output += "</" + tag + ">"
                self.current_block = "tag"
            elif tag not in self.self_closing_tags:
                self.output = self.output.rstrip()
                if self.output != "":
                    self.output = self.output + "\n"

                # print("end")
                self.level -= 1
                self.output += (self.indent * self.level) + "</" + tag + ">\n"
                self.current_block = "tag"


        def handle_tempstateendtag(self, tag, attrs):
            attribs = (" " + (" ").join(attrs) + "" if attrs else "")
            if tag in self.indent_temp_tags:
                self.level -= 1
                self.output += (self.indent * self.level) + "{% end" + tag + " %}\n"

        def handle_data(self, data):
            if self.ignored_level > 0 or self.inline_level > 0 and data.strip() != "":
                self.output += data
                self.current_block = "text"
            elif data.strip() != "":

                if breakbefore(self.output):
                    self.output += (self.indent * self.level)
                self.output += re.sub(r"\s+$", " ",data.lstrip(), re.M)
                self.current_block = "text"

        def handle_comment(self, data):
            if breakbefore(self.output):
                self.output += (self.indent * self.level)
            elif self.ignored_level == 0 and self.inline_level == 0 and not breakbefore(self.output):
                self.output += "\n" + (self.indent * self.level)
            self.output += "<!--"+ data + "-->"


        def close(self):
            super(MyHTMLParser,self).close()
            return self.output


    p = MyHTMLParser()
    p.feed(rawcode)
    output = p.close()



    output = front_matter + output

    return output
