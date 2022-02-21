from .parser import HTMLParser
import re
rawcode = """<P>
    some nice text <a href="this">asdf</a>, ok
</p>"""
#rawcode = """<div class="a" id="b"></div>"""

def indent_html(rawcode, config):

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


    ## pop front mater
    rawcode = rawcode.strip()

    front_matter = re.search(r'^---[\s\S]+?---\S*', rawcode)

    if front_matter:
        front_matter = front_matter.group()
        rawcode = rawcode.replace(front_matter,"")
        front_matter = front_matter.strip() + "\n"
    else:
        front_matter = ""

    p = MyHTMLParser()
    p.feed(rawcode)
    p.close()


    indent_html_tags = ["div", "p", "dd"]
    ignored_html_tags = ["pre","code", 'textarea', 'script']
    inline_blocks = ["h1","h2","h3","h4","h5",'h6', "a", "span", "input", "small"]
    indent_temp_tags = ["if"]
    indent_block = False
    current_block = "tag"

    indent = "    "
    level = 0
    ignored_level = 0
    inline_level = 0
    is_inline = False

    def breakbefore(html):

        return bool(re.search(r"\n[ \t]*$",html, re.M))

    def spacebefore(html):
        return bool(re.search(r"[ ]*$",html, re.M))

    output = ""
    for el in elements:
        #print(el)

        if el.get("type") == "HTML":
            attribs = (" " + (" ").join([x[0] + "=\"" + x[1] + "\"" for x in el["attrs"]]) + "" if el.get("attrs") else "")


            if el.get("tag") in indent_html_tags:
                output = output.rstrip()
                if output != "":
                    output = output + "\n"

                if el["location"] == "START":

                    output += (indent * level) + "<" + el.get("tag") + attribs + ">\n"
                    level += 1
                elif el["location"] == "END":
                    print("end")
                    level -= 1
                    output += (indent * level) + "</" + el.get("tag") + ">\n"
                current_block = "tag"

            elif el.get("tag") in ignored_html_tags:

                if el["location"] == "START":
                    if ignored_level == 0 and breakbefore(output):
                        output += (indent * level)
                    elif ignored_level == 0 and not breakbefore(output):
                        output += "\n" + (indent * level)
                    output += "<" + el.get("tag") + attribs+ ">"
                    ignored_level += 1
                elif el["location"] == "END":
                    output += "</" + el.get("tag") + ">"
                    ignored_level -= 1
                current_block = "tag"


            elif el.get("tag") in inline_blocks:

                if el["location"] == "START":
                    if inline_level == 0 and breakbefore(output):
                        output += (indent * level)

                    print(inline_level)
                    print(output)
                    print(breakbefore(output))
                    print(current_block)
                    if inline_level == 0 and not breakbefore(output) and current_block=="tag":
                        output += "\n" + (indent * level)

                    inline_level += 1
                    output += "<" + el.get("tag") +attribs + ">"
                elif el["location"] == "END":
                    inline_level -= 1
                    output += "</" + el.get("tag") + ">"

                current_block = "tag"


            elif el.get('comment'):
                if breakbefore(output):
                    output += (indent * level)
                elif ignored_level == 0 and inline_level == 0 and not breakbefore(output):
                    output += "\n" + (indent * level)
                output += "<!--"+ el["comment"] + "-->"

            else:
                assert 1==2
                if el["location"] == "START":
                    output += (indent * level) + "<" + el.get("tag") + attribs +">"
                elif el["location"] == "END":
                    output += "</" + el.get("tag") + ">"
                current_block = "tag"



        elif el.get("type") == "CURLY_STATEMENT":
            attribs = (" " + (" ").join(el["attrs"]) + "" if el.get("attrs") else "")
            if el.get("tag") in indent_temp_tags:
                if el["location"] == "START":
                    output += (indent * level) + "{% " + el.get("tag") + attribs +" %}\n"
                    level += 1
                elif el["location"] == "END":
                    level -= 1
                    output += (indent * level) + "{% end" + el.get("tag") + " %}\n"


        elif el.get('data'):
            if ignored_level > 0 or inline_level > 0 and el.get('data').strip() != "":
                output += el.get('data')
                current_block = "text"
            elif el.get('data').strip() != "":

                if breakbefore(output):
                    output += (indent * level)
                output += re.sub(r"\s+$", " ",el.get('data').lstrip(), re.M)
                current_block = "text"


    output = front_matter + output

    return output
