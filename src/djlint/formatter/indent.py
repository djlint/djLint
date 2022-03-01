from .parser import HTMLParser
import re

def indent_html(rawcode, config):

    ## pop front mater
    rawcode = rawcode.strip()

    front_matter = re.search(r'^---[\s\S]+?---\S*', rawcode)

    if front_matter:
        front_matter = front_matter.group()
        rawcode = rawcode.replace(front_matter,"")
        front_matter = front_matter.strip() + "\n"
    else:
        front_matter = ""



    def breakbefore(html):

        return bool(re.search(r"\n[ \t]*$",html, re.M))

    def spacebefore(html):
        return bool(re.search(r"[ ]*$",html, re.M))



    elements = []

    class MyHTMLParser(HTMLParser):


        def __init__(self):
            super(MyHTMLParser,self).__init__()
            self.output = ""
            self.indent_html_tags = ["div", "p", "dd"]
            self.ignored_html_tags = ["pre","code", 'textarea', 'script']
            self.inline_blocks = ["h1","h2","h3","h4","h5",'h6', "a", "span", "input", "small"]
            self.indent_temp_tags = ["if"]
            self.indent_block = False
            self.current_block = "tag"

            self.indent = "    "
            self.level = 0
            self.ignored_level = 0
            self.inline_level = 0
            self.is_inline = False

        def handle_starttag(self, tag, attrs):
            attribs = (" " + (" ").join([x[0] + "=\"" + x[1] + "\"" for x in attrs]) + "" if attrs else "")

            if tag in self.indent_html_tags:
                self.output = self.output.rstrip()
                if self.output != "":
                    self.output = self.output + "\n"

                self.output += (self.indent * self.level) + "<" + tag + attribs + ">\n"
                self.level += 1
                self.current_block = "tag"

            elif tag in self.ignored_html_tags:
                if self.ignored_level == 0 and breakbefore(self.output):
                    self.output += (self.indent * self.level)
                elif self.ignored_level == 0 and not breakbefore(self.output):
                    self.output += "\n" + (self.indent * self.level)
                self.output += "<" + tag + attribs+ ">"
                self.ignored_level += 1
                self.current_block = "tag"

            elif tag in self.inline_blocks:
                if self.inline_level == 0 and breakbefore(self.output):
                    self.output += (self.indent * self.level)

                print(self.inline_level)
                print(self.output)
                print(breakbefore(self.output))
                print(self.current_block)
                if self.inline_level == 0 and not breakbefore(self.output) and self.current_block=="tag":
                    self.output += "\n" + (self.indent * self.level)

                self.inline_level += 1
                self.output += "<" + tag +attribs + ">"
                self.current_block = "tag"

        def handle_tempstatestarttag(self, tag, attrs):
            attribs = (" " + (" ").join(attrs) + "" if attrs else "")
            if tag in self.indent_temp_tags:
                self.output += (self.indent * self.level) + "{% " + tag + attribs +" %}\n"
                self.level += 1

        def handle_endtag(self, tag):


            if tag in self.indent_html_tags:
                self.output = self.output.rstrip()
                if self.output != "":
                    self.output = self.output + "\n"

                print("end")
                self.level -= 1
                self.output += (self.indent * self.level) + "</" + tag + ">\n"
                self.current_block = "tag"
            elif tag in self.ignored_html_tags:
                self.output += "</" + tag + ">"
                self.ignored_level -= 1
                self.current_block = "tag"

            elif tag in self.inline_blocks:
                self.inline_level -= 1
                self.output += "</" + tag + ">"
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
