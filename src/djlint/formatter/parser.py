"""A parser for HTML and XHTML."""

# This file is based on sgmllib.py, but the API is slightly different.

# XXX There should be a way to distinguish between PCDATA (parsed
# character data -- the normal case), RCDATA (replaceable character
# data -- only char and entity references and end tags are special)
# and CDATA (character data -- only end tags are special).
# https://github.com/python/cpython/blob/3.10/Lib/html/parser.py

import re

import _markupbase

from html import unescape


__all__ = ['HTMLParser']


_declname_match = re.compile(r'[a-zA-Z][-_.a-zA-Z0-9]*\s*').match
_declstringlit_match = re.compile(r'(\'[^\']*\'|"[^"]*")\s*').match
_commentclose = re.compile(r'--\s*>')
_markedsectionclose = re.compile(r']\s*]\s*>')

# An analysis of the MS-Word extensions is available at
# http://www.planetpublish.com/xmlarena/xap/Thursday/WordtoXML.pdf

_msmarkedsectionclose = re.compile(r']\s*>')

# Regular expressions used for parsing

interesting_normal = re.compile('[&<]')
incomplete = re.compile('&[a-zA-Z#]')

entityref = re.compile('&([a-zA-Z][-.a-zA-Z0-9]*)[^a-zA-Z0-9]')
charref = re.compile('&#(?:[0-9]+|[xX][0-9a-fA-F]+)[^0-9a-fA-F]')

starttagopen = re.compile('<[a-zA-Z]')
starttempstateopen = re.compile(r'{%')
endtempstateopen = re.compile(r'{%\s*end', re.I)
starttempopen = re.compile('{{')

piclose = re.compile('>')
commentclose = re.compile(r'--\s*>')

# Note:
#  1) if you change tagfind/attrfind remember to update locatestarttagend too;
#  2) if you change tagfind/attrfind and/or locatestarttagend the parser will
#     explode, so don't do it.
# see http://www.w3.org/TR/html5/tokenization.html#tag-open-state
# and http://www.w3.org/TR/html5/tokenization.html#tag-name-state

tagfind_tolerant = re.compile(r'([a-zA-Z][^\t\n\r\f />\x00]*)(?:\s|/(?!>))*')
tempstatetagfind_tolerant = re.compile(r'(\s*[a-zA-Z](?:(?!%}|\t|\n|\r|\f| |\x00).)*)(?:\s|/(?!%}))*')
attrfind_tolerant = re.compile(
    r'((?<=[\'"\s/])[^\s/>][^\s/=>]*)(\s*=+\s*'
    r'(\'[^\']*\'|"[^"]*"|(?![\'"])[^>\s]*))?(?:\s|/(?!>))*')
tempstateattrfind_tolerant = re.compile(
    r'((?<=[\'"\s/])(?:(?!%}|\s|/).)(?:(?!%}|\s|/|=).)*)(\s*=+\s*(\'[^\']*\'|"[^"]*"|(?![\'"])(?:(?!%}|\s).)*))?(?:\s|/(?!%}))*')
locatestarttagend_tolerant = re.compile(r"""
  <[a-zA-Z][^\t\n\r\f />\x00]*       # tag name
  (?:[\s/]*                          # optional whitespace before attribute name
    (?:(?<=['"\s/])[^\s/>][^\s/=>]*  # attribute name
      (?:\s*=+\s*                    # value indicator
        (?:'[^']*'                   # LITA-enclosed value
          |"[^"]*"                   # LIT-enclosed value
          |(?!['"])[^>\s]*           # bare value
         )
        \s*                          # possibly followed by a space
       )?(?:\s|/(?!>))*
     )*
   )?
  \s*                                # trailing whitespace
""", re.VERBOSE)

locatestarttempstateend_tolerant = re.compile(r"""

  {%[\s/]*[a-zA-Z](?:(?!%}|\t|\n|\r|\f| |\x00).)*       # tag name
  (?:[\s/]*                                             # optional whitespace before attribute name
    (?:'[^']*'                   # LITA-enclosed value
      |"[^"]*"                   # LIT-enclosed value
      |(?!['"])(?:(?!%}|\s).)*       # bare value
    )*
  )*
  \s*                                # trailing whitespace
""", re.VERBOSE)

locatestarttempend_tolerant = re.compile(r"""
  {{[\s/]*[a-zA-Z](?:(?!}}|\t|\n|\r|\f| |\x00).)*       # tag name
  (?:[\s/]*                                             # optional whitespace before attribute name
    (?:(?!\s}}.)*)                                       # attribute name
  )
  \s*                                # trailing whitespace
""", re.VERBOSE)

endendtag = re.compile('>')
endtempstateendtag = re.compile('%}')
# the HTML 5 spec, section 8.1.2.2, doesn't allow spaces between
# </ and the tag name, so maybe this should be fixed
endtagfind = re.compile(r'</\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\s*>')
endtempstatetagfind = re.compile(r'{%\s*end([a-zA-Z][-.a-zA-Z0-9:_]*)\s*%}', re.I)



class HTMLParser(_markupbase.ParserBase):
    """Find tags and other markup and call handler functions.

    Usage:
        p = HTMLParser()
        p.feed(data)
        ...
        p.close()

    Start tags are handled by calling self.handle_starttag() or
    self.handle_startendtag(); end tags by self.handle_endtag().  The
    data between tags is passed from the parser to the derived class
    by calling self.handle_data() with the data as argument (the data
    may be split up in arbitrary chunks).  If convert_charrefs is
    True the character references are converted automatically to the
    corresponding Unicode character (and self.handle_data() is no
    longer split in chunks), otherwise they are passed by calling
    self.handle_entityref() or self.handle_charref() with the string
    containing respectively the named or numeric reference as the
    argument.
    """

    CDATA_CONTENT_ELEMENTS = ("script", "style")

    def __init__(self, *, convert_charrefs=True):
        """Initialize and reset this instance.

        If convert_charrefs is True (the default), all character references
        are automatically converted to the corresponding Unicode characters.
        """
        self.convert_charrefs = convert_charrefs
        self.reset()

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.lineno = 1
        self.offset = 0
        self.rawdata = ''
        self.lasttag = '???'

        self.interesting = interesting_normal
        self.cdata_elem = None
        _markupbase.ParserBase.reset(self)

    def getpos(self):
        """Return current line number and offset."""
        return self.lineno, self.offset

    # Internal -- update line number and offset.  This should be
    # called for each piece of data exactly once, in order -- in other
    # words the concatenation of all the input strings to this
    # function should be exactly the entire input.
    def updatepos(self, i, j):
        if i >= j:
            return j
        rawdata = self.rawdata
        nlines = rawdata.count("\n", i, j)
        if nlines:
            self.lineno = self.lineno + nlines
            pos = rawdata.rindex("\n", i, j) # Should not fail
            self.offset = j-(pos+1)
        else:
            self.offset = self.offset + j-i
        return j

    _decl_otherchars = ''


    def feed(self, data):
        r"""Feed data to the parser.

        Call this as often as you want, with as little or as much text
        as you want (may include '\n').
        """
        self.rawdata = self.rawdata + data
        self.goahead(0)

    def close(self):
        """Handle any buffered data."""
        self.goahead(1)

    __starttag_text = None

    def get_starttag_text(self):
        """Return full source of start tag: '<...>'."""
        return self.__starttag_text

    def set_cdata_mode(self, elem):
        self.cdata_elem = elem.lower()
        self.interesting = re.compile(r'</\s*%s\s*>' % self.cdata_elem, re.I)

    def clear_cdata_mode(self):
        self.interesting = interesting_normal
        self.cdata_elem = None

    # Internal -- handle data as far as reasonable.  May leave state
    # and data to be processed by a subsequent call.  If 'end' is
    # true, force handling all data as if followed by EOF marker.
    def goahead(self, end):
        rawdata = self.rawdata
        i = 0
        n = len(rawdata)
        while i < n:
            if self.convert_charrefs and not self.cdata_elem:

                start_match = re.search(r"<|{%", rawdata[i:])
                j = (
                      start_match.start() + i if start_match else -1
                    )


                if j < 0:
                    # if we can't find the next <, either we are at the end
                    # or there's more text incoming.  If the latter is True,
                    # we can't pass the text to handle_data in case we have
                    # a charref cut in half at end.  Try to determine if
                    # this is the case before proceeding by looking for an
                    # & near the end and see if it's followed by a space or ;.
                    amppos = rawdata.rfind('&', max(i, n-34))
                    if (amppos >= 0 and
                        not re.compile(r'[\s;]').search(rawdata, amppos)):

                        break  # wait till we get all the text
                    j = n
            else:
                match = self.interesting.search(rawdata, i)  # < or &
                if match:
                    j = match.start()
                else:
                    if self.cdata_elem:
                        break
                    j = n
            if i < j:
                if self.convert_charrefs and not self.cdata_elem:
                    self.handle_data(unescape(rawdata[i:j]))
                else:
                    self.handle_data(rawdata[i:j])
            i = self.updatepos(i, j)
            if i == n: break
            startswith = rawdata.startswith
            if startswith('<', i):
                if starttagopen.match(rawdata, i): # < + letter
                    k = self.parse_starttag(i)
                elif startswith("</", i):
                    k = self.parse_endtag(i)
                elif startswith("<!--", i):
                    k = self.parse_comment(i)
                elif startswith("<?", i):
                    k = self.parse_pi(i)
                elif startswith("<!", i):
                    k = self.parse_html_declaration(i)
                elif (i + 1) < n:
                    self.handle_data("<")
                    k = i + 1
                else:
                    break
                if k < 0:
                    if not end:
                        break

                    k = rawdata.find('>', i + 1)
                    if k < 0:
                        k = rawdata.find('<', i + 1)

                        if k < 0:
                            k = i + 1
                    else:
                        k += 1
                    if self.convert_charrefs and not self.cdata_elem:
                        self.handle_data(unescape(rawdata[i:k]))
                    else:
                        self.handle_data(rawdata[i:k])
                i = self.updatepos(i, k)
            elif startswith("&#", i):
                match = charref.match(rawdata, i)
                if match:
                    name = match.group()[2:-1]
                    self.handle_charref(name)
                    k = match.end()

                    if not startswith(';', k-1):

                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                else:
                    if ";" in rawdata[i:]:  # bail by consuming &#
                        self.handle_data(rawdata[i:i+2])
                        i = self.updatepos(i, i+2)
                    break
            elif startswith('&', i):

                match = entityref.match(rawdata, i)
                if match:
                    name = match.group(1)
                    self.handle_entityref(name)
                    k = match.end()
                    if not startswith(';', k-1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                match = incomplete.match(rawdata, i)
                if match:
                    # match.group() will contain at least 2 chars
                    if end and match.group() == rawdata[i:]:
                        k = match.end()
                        if k <= i:
                            k = n
                        i = self.updatepos(i, i + 1)
                    # incomplete
                    break
                elif (i + 1) < n:
                    # not the end of the buffer, and can't be confused
                    # with some other construct
                    self.handle_data("&")
                    i = self.updatepos(i, i + 1)
                else:
                    break
            elif startswith("{%", i):
                # end first
                if endtempstateopen.match(rawdata, i):
                    k = self.parse_tempstateendtag(i)
                elif starttempstateopen.match(rawdata, i):
                    k = self.parse_tempstatestarttag(i)

                if k < 0:
                    if not end:
                        break
                    k = rawdata.find('%}', i + 1)
                    if k < 0:
                        k = rawdata.find('{%', i + 1)
                        if k < 0:
                            k = i + 1
                    else:
                        k += 1
                    if self.convert_charrefs and not self.cdata_elem:
                        self.handle_data(unescape(rawdata[i:k]))
                    else:
                        self.handle_data(rawdata[i:k])

                i = self.updatepos(i, k)
            else:
                assert 0, "interesting.search() lied"
        # end while
        if end and i < n and not self.cdata_elem:
            if self.convert_charrefs and not self.cdata_elem:
                self.handle_data(unescape(rawdata[i:n]))
            else:
                self.handle_data(rawdata[i:n])
            i = self.updatepos(i, n)
        self.rawdata = rawdata[i:]

    # Internal -- parse html declarations, return length or -1 if not terminated
    # See w3.org/TR/html5/tokenization.html#markup-declaration-open-state
    # See also parse_declaration in _markupbase
    def parse_html_declaration(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i+2] == '<!', ('unexpected call to '
                                        'parse_html_declaration()')
        if rawdata[i:i+4] == '<!--':
            # this case is actually already handled in goahead()
            return self.parse_comment(i)
        elif rawdata[i:i+3] == '<![':
            return self.parse_marked_section(i)
        elif rawdata[i:i+9].lower() == '<!doctype':
            # find the closing >
            gtpos = rawdata.find('>', i+9)
            if gtpos == -1:
                return -1
            self.handle_decl(rawdata[i+2:gtpos])
            return gtpos+1
        else:
            return self.parse_bogus_comment(i)

    # Internal -- parse bogus comment, return length or -1 if not terminated
    # see http://www.w3.org/TR/html5/tokenization.html#bogus-comment-state
    def parse_bogus_comment(self, i, report=1):
        rawdata = self.rawdata

        assert rawdata[i:i+2] in ('<!', '</'), ('unexpected call to '
                                                'parse_comment()')
        pos = rawdata.find('>', i+2)
        if pos == -1:
            return -1
        if report:
            self.handle_comment(rawdata[i+2:pos], "HTML")

        return pos + 1

    # Internal -- parse processing instr, return end or -1 if not terminated
    def parse_pi(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i+2] == '<?', 'unexpected call to parse_pi()'
        match = piclose.search(rawdata, i+2) # >
        if not match:
            return -1
        j = match.start()
        self.handle_pi(rawdata[i+2: j])

        j = match.end()
        return j

    # Internal -- handle starttag, return end or -1 if not terminated
    def parse_starttag(self, i):
        self.__starttag_text = None
        endpos = self.check_for_whole_start_tag(i)
        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[i:endpos]

        # Now parse the data between i+1 and j into a tag and attrs
        attrs = []
        match = tagfind_tolerant.match(rawdata, i+1)

        assert match, 'unexpected call to parse_starttag()'
        k = match.end()
        self.lasttag = tag = match.group(1).lower()
        while k < endpos:
            m = attrfind_tolerant.match(rawdata, k)

            if not m:
                break
            attrname, rest, attrvalue = m.group(1, 2, 3)
            if not rest:
                attrvalue = None
            elif attrvalue[:1] == '\'' == attrvalue[-1:] or \
                 attrvalue[:1] == '"' == attrvalue[-1:]:
                attrvalue = attrvalue[1:-1]
            if attrvalue:
                attrvalue = unescape(attrvalue)
            attrs.append((attrname.lower(), attrvalue))
            k = m.end()
        end = rawdata[k:endpos].strip()
        if end not in (">", "/>"):
            lineno, offset = self.getpos()
            if "\n" in self.__starttag_text:
                lineno = lineno + self.__starttag_text.count("\n")
                offset = len(self.__starttag_text) \
                         - self.__starttag_text.rfind("\n")
            else:
                offset = offset + len(self.__starttag_text)
            self.handle_data(rawdata[i:endpos])
            return endpos
        if end.endswith('/>'):
            # XHTML-style empty tag: <span attr="value" />
            self.handle_startendtag(tag, attrs)
        else:
            self.handle_starttag(tag, attrs)
            if tag in self.CDATA_CONTENT_ELEMENTS:
                self.set_cdata_mode(tag)
        return endpos

    # Internal -- handle starttag, return end or -1 if not terminated
    def parse_tempstatestarttag(self, i):
        self.__starttag_text = None
        endpos = self.check_for_whole_temp_state_start_tag(i)

        if endpos < 0:
            return endpos
        rawdata = self.rawdata
        self.__starttag_text = rawdata[i:endpos]

        # Now parse the data between i+1 and j into a tag and attrs
        attrs = []
        match = tempstatetagfind_tolerant.match(rawdata, i+2) # start tag is 2 chars wide
        assert match, 'unexpected call to parse_tempstatestarttag()'
        k = match.end()

        self.lasttag = tag = match.group(1).lower()
        while k < endpos:
            m = tempstateattrfind_tolerant.match(rawdata, k)
            if not m:
                break

            attr = m.group(1)

            attrs.append(attr)
            k = m.end()

        end = rawdata[k:endpos].strip()
        if end != "%}":
            lineno, offset = self.getpos()
            if "\n" in self.__starttag_text:
                lineno = lineno + self.__starttag_text.count("\n")
                offset = len(self.__starttag_text) \
                         - self.__starttag_text.rfind("\n")
            else:
                offset = offset + len(self.__starttag_text)
            self.handle_data(rawdata[i:endpos])
            return endpos
        # statement tags are not else ending.
        # if end.endswith('%}'):
        #     # XHTML-style empty tag: <span attr="value" />
        #     self.handle_tempstatestartendtag(tag, attrs)
        #else:
        self.handle_tempstatestarttag(tag.strip(), attrs)
        if tag in self.CDATA_CONTENT_ELEMENTS:
            self.set_cdata_mode(tag)
        return endpos

    # Internal -- check to see if we have a complete starttag; return end
    # or -1 if incomplete.
    def check_for_whole_start_tag(self, i):
        rawdata = self.rawdata
        m = locatestarttagend_tolerant.match(rawdata, i)

        if m:
            j = m.end()
            next = rawdata[j:j+1]

            if next == ">":
                return j + 1
            if next == "/":
                if rawdata.startswith("/>", j):
                    return j + 2
                if rawdata.startswith("/", j):
                    # buffer boundary
                    return -1
                # else bogus input
                if j > i:
                    return j
                else:
                    return i + 1
            if next == "%":
                if rawdata.startswith("%}", j):
                    return j + 2
                if rawdata.startswith("%", j):
                    # buffer boundary
                    return -1
            if next == "}":
                if rawdata.startswith("}}", j):
                    return j + 2
                if rawdata.startswith("}", j):
                    # buffer boundary
                    return -1
            if next == "":
                # end of input
                return -1
            if next in ("abcdefghijklmnopqrstuvwxyz=/"
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                # end of input in or before attribute value, or we have the
                # '/' from a '/>' ending
                return -1
            if j > i:
                return j
            else:
                return i + 1
        raise AssertionError("we should not get here!")

    def check_for_whole_temp_state_start_tag(self, i):
        rawdata = self.rawdata

        m = locatestarttempstateend_tolerant.match(rawdata, i)

        if m:
            j = m.end()
            next = rawdata[j:j+1]

            if next == "%":
                if rawdata.startswith("%}", j):
                    return j + 2
                if rawdata.startswith("%", j):
                    # buffer boundary
                    return -1
            if next == "":
                # end of input
                return -1
            if next in ("abcdefghijklmnopqrstuvwxyz=/"
                        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                # end of input in or before attribute value, or we have the
                # '/' from a '/>' ending
                return -1
            if j > i:
                return j
            else:
                return i + 1
        raise AssertionError("we should not get here!")

    # Internal -- parse endtag, return end or -1 if incomplete
    def parse_endtag(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i+2] == "</", "unexpected call to parse_endtag"
        match = endendtag.search(rawdata, i+1) # >
        if not match:
            return -1
        gtpos = match.end()
        match = endtagfind.match(rawdata, i) # </ + tag + >

        if not match:
            if self.cdata_elem is not None:
                self.handle_data(rawdata[i:gtpos])
                return gtpos
            # find the name: w3.org/TR/html5/tokenization.html#tag-name-state
            namematch = tagfind_tolerant.match(rawdata, i+2)
            if not namematch:
                # w3.org/TR/html5/tokenization.html#end-tag-open-state
                if rawdata[i:i+3] == '</>':
                    return i+3

                else:
                    return self.parse_bogus_comment(i)
            tagname = namematch.group(1).lower()
            # consume and ignore other stuff between the name and the >
            # Note: this is not 100% correct, since we might have things like
            # </tag attr=">">, but looking for > after the name should cover
            # most of the cases and is much simpler
            gtpos = rawdata.find('>', namematch.end())
            self.handle_endtag(tagname)
            return gtpos+1

        elem = match.group(1).lower() # script or style

        if self.cdata_elem is not None:
            if elem != self.cdata_elem:
                self.handle_data(rawdata[i:gtpos])
                return gtpos


        self.handle_endtag(elem)

        self.clear_cdata_mode()
        return gtpos

    # Internal -- parse endtag, return end or -1 if incomplete
    def parse_tempstateendtag(self, i):
        rawdata = self.rawdata
        assert rawdata[i:i+2] == "{%", "unexpected call to parse_endtag"
        match = endtempstateendtag.search(rawdata, i+2) # %}
        if not match:
            return -1
        gtpos = match.end()
        match = endtempstatetagfind.match(rawdata, i) # </ + tag + >

        if not match:
            if self.cdata_elem is not None:
                self.handle_data(rawdata[i:gtpos])
                return gtpos
            # find the name: w3.org/TR/html5/tokenization.html#tag-name-state
            namematch = tempstatetagfind_tolerant.match(rawdata, i+2)
            if not namematch:
                # w3.org/TR/html5/tokenization.html#end-tag-open-state
                if rawdata[i:i+3] == '</>':
                    return i+3

                else:
                    return self.parse_bogus_comment(i)
            tagname = namematch.group(1).lower()
            # consume and ignore other stuff between the name and the >
            # Note: this is not 100% correct, since we might have things like
            # </tag attr=">">, but looking for > after the name should cover
            # most of the cases and is much simpler
            gtpos = rawdata.find('%}', namematch.end())
            self.handle_tempstateendtag(tagname)
            return gtpos+1

        elem = match.group(1).lower() # script or style

        if self.cdata_elem is not None:
            if elem != self.cdata_elem:
                self.handle_data(rawdata[i:gtpos])
                return gtpos

        self.handle_tempstateendtag(elem)
        self.clear_cdata_mode()
        return gtpos

    # Internal -- parse declaration (for use by subclasses).
    def parse_declaration(self, i):
        # This is some sort of declaration; in "HTML as
        # deployed," this should only be the document type
        # declaration ("<!DOCTYPE html...>").
        # ISO 8879:1986, however, has more complex
        # declaration syntax for elements in <!...>, including:
        # --comment--
        # [marked section]
        # name in the following list: ENTITY, DOCTYPE, ELEMENT,
        # ATTLIST, NOTATION, SHORTREF, USEMAP,
        # LINKTYPE, LINK, IDLINK, USELINK, SYSTEM
        rawdata = self.rawdata
        j = i + 2
        assert rawdata[i:j] == "<!", "unexpected call to parse_declaration"
        if rawdata[j:j+1] == ">":
            # the empty comment <!>
            return j + 1
        if rawdata[j:j+1] in ("-", ""):

            # Start of comment followed by buffer boundary,
            # or just a buffer boundary.
            return -1
        # A simple, practical version could look like: ((name|stringlit) S*) + '>'
        n = len(rawdata)
        if rawdata[j:j+2] == '--': #comment
            # Locate --.*-- as the body of the comment
            return self.parse_comment(i)
        elif rawdata[j] == '[': #marked section

            # Locate [statusWord [...arbitrary SGML...]] as the body of the marked section
            # Where statusWord is one of TEMP, CDATA, IGNORE, INCLUDE, RCDATA
            # Note that this is extended by Microsoft Office "Save as Web" function
            # to include [if...] and [endif].
            return self.parse_marked_section(i)
        else: #all other declaration elements

            decltype, j = self._scan_name(j, i)
        if j < 0:
            return j
        if decltype == "doctype":
            self._decl_otherchars = ''

        while j < n:
            c = rawdata[j]
            if c == ">":
                # end of declaration syntax
                data = rawdata[i+2:j]

                if decltype == "doctype":
                    self.handle_decl(data)
                else:
                    # According to the HTML5 specs sections "8.2.4.44 Bogus
                    # comment state" and "8.2.4.45 Markup declaration open
                    # state", a comment token should be emitted.
                    # Calling unknown_decl provides more flexibility though.
                    self.unknown_decl(data)
                return j + 1
            if c in "\"'":
                m = _declstringlit_match(rawdata, j)
                if not m:
                    return -1 # incomplete

                j = m.end()
            elif c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
                name, j = self._scan_name(j, i)
            elif c in self._decl_otherchars:
                j = j + 1
            elif c == "[":
                # this could be handled in a separate doctype parser
                if decltype == "doctype":
                    j = self._parse_doctype_subset(j + 1, i)
                elif decltype in {"attlist", "linktype", "link", "element"}:
                    # must tolerate []'d groups in a content model in an element declaration
                    # also in data attribute specifications of attlist declaration
                    # also link type declaration subsets in linktype declarations
                    # also link attribute specification lists in link declarations
                    raise AssertionError("unsupported '[' char in %s declaration" % decltype)

                else:
                    raise AssertionError("unexpected '[' char in declaration")
            else:
                raise AssertionError("unexpected %r char in declaration" % rawdata[j])
            if j < 0:
                return j
        return -1 # incomplete

    # Internal -- parse a marked section
    # Override this to handle MS-word extension syntax <![if word]>content<![endif]>
    def parse_marked_section(self, i, report=1):

        rawdata= self.rawdata
        assert rawdata[i:i+3] == '<![', "unexpected call to parse_marked_section()"
        sectName, j = self._scan_name( i+3, i )

        if j < 0:
            return j
        if sectName in {"temp", "cdata", "ignore", "include", "rcdata"}:
            # look for standard ]]> ending

            match= _markedsectionclose.search(rawdata, i+3)
        elif sectName in {"if", "else", "endif"}:
            # look for MS Office ]> ending
            match= _msmarkedsectionclose.search(rawdata, i+3)
        else:
            raise AssertionError(
                'unknown status keyword %r in marked section' % rawdata[i+3:j]

            )
        if not match:
            return -1
        if report:
            j = match.start(0)

            self.unknown_decl(rawdata[i+3: j])

        return match.end(0)

    # Internal -- parse comment, return length or -1 if not terminated
    def parse_comment(self, i, report=1):
        rawdata = self.rawdata

        if rawdata[i:i+4] != '<!--':
            raise AssertionError('unexpected call to parse_comment()')
        match = _commentclose.search(rawdata, i+4)

        if not match:
            return -1
        if report:
            j = match.start(0)

            self.handle_comment(rawdata[i+4: j])

        return match.end(0)

    # Internal -- scan past the internal subset in a <!DOCTYPE declaration,
    # returning the index just past any whitespace following the trailing ']'.
    def _parse_doctype_subset(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        j = i
        while j < n:
            c = rawdata[j]
            if c == "<":

                s = rawdata[j:j+2]

                if s == "<":
                    # end of buffer; incomplete
                    return -1
                if s != "<!":
                    self.updatepos(declstartpos, j + 1)
                    raise AssertionError(
                        "unexpected char in internal subset (in %r)" % s
                    )
                if (j + 2) == n:
                    # end of buffer; incomplete
                    return -1
                if (j + 4) > n:
                    # end of buffer; incomplete
                    return -1

                if rawdata[j:j+4] == "<!--":

                    j = self.parse_comment(j, report=0)
                    if j < 0:
                        return j
                    continue
                name, j = self._scan_name(j + 2, declstartpos)
                if j == -1:
                    return -1
                if name not in {"attlist", "element", "entity", "notation"}:
                    self.updatepos(declstartpos, j + 2)
                    raise AssertionError(
                        "unknown declaration %r in internal subset" % name
                    )
                # handle the individual names
                meth = getattr(self, "_parse_doctype_" + name)
                j = meth(j, declstartpos)
                if j < 0:
                    return j
            elif c == "%":
                # parameter entity reference
                if (j + 1) == n:
                    # end of buffer; incomplete
                    return -1
                s, j = self._scan_name(j + 1, declstartpos)
                if j < 0:
                    return j
                if rawdata[j] == ";":
                    j = j + 1
            elif c == "]":
                j = j + 1
                while j < n and rawdata[j].isspace():
                    j = j + 1
                if j < n:
                    if rawdata[j] == ">":
                        return j
                    self.updatepos(declstartpos, j)
                    raise AssertionError("unexpected char after internal subset")
                else:
                    return -1
            elif c.isspace():
                j = j + 1
            else:
                self.updatepos(declstartpos, j)
                raise AssertionError("unexpected char %r in internal subset" % c)
        # end of buffer reached
        return -1

    # Internal -- scan past <!ELEMENT declarations
    def _parse_doctype_element(self, i, declstartpos):
        name, j = self._scan_name(i, declstartpos)
        if j == -1:
            return -1
        # style content model; just skip until '>'
        rawdata = self.rawdata

        if '>' in rawdata[j:]:

            return rawdata.find(">", j) + 1
        return -1

    # Internal -- scan past <!ATTLIST declarations
    def _parse_doctype_attlist(self, i, declstartpos):
        rawdata = self.rawdata
        name, j = self._scan_name(i, declstartpos)

        c = rawdata[j:j+1]

        if c == "":
            return -1
        if c == ">":
            return j + 1
        while 1:
            # scan a series of attribute descriptions; simplified:
            #   name type [value] [#constraint]
            name, j = self._scan_name(j, declstartpos)
            if j < 0:
                return j

            c = rawdata[j:j+1]

            if c == "":
                return -1
            if c == "(":
                # an enumerated type; look for ')'
                if ")" in rawdata[j:]:
                    j = rawdata.find(")", j) + 1
                else:
                    return -1

                while rawdata[j:j+1].isspace():

                    j = j + 1
                if not rawdata[j:]:
                    # end of buffer, incomplete
                    return -1
            else:
                name, j = self._scan_name(j, declstartpos)

            c = rawdata[j:j+1]

            if not c:
                return -1
            if c in "'\"":
                m = _declstringlit_match(rawdata, j)
                if m:
                    j = m.end()
                else:
                    return -1

                c = rawdata[j:j+1]

                if not c:
                    return -1
            if c == "#":
                if rawdata[j:] == "#":
                    # end of buffer
                    return -1
                name, j = self._scan_name(j + 1, declstartpos)
                if j < 0:
                    return j

                c = rawdata[j:j+1]
                if not c:
                    return -1
            if c == '>':

                # all done
                return j + 1

    # Internal -- scan past <!NOTATION declarations
    def _parse_doctype_notation(self, i, declstartpos):
        name, j = self._scan_name(i, declstartpos)
        if j < 0:
            return j
        rawdata = self.rawdata
        while 1:

            c = rawdata[j:j+1]
            if not c:
                # end of buffer; incomplete
                return -1
            if c == '>':

                return j + 1
            if c in "'\"":
                m = _declstringlit_match(rawdata, j)
                if not m:
                    return -1
                j = m.end()
            else:
                name, j = self._scan_name(j, declstartpos)
                if j < 0:
                    return j

    # Internal -- scan past <!ENTITY declarations
    def _parse_doctype_entity(self, i, declstartpos):
        rawdata = self.rawdata

        if rawdata[i:i+1] == "%":
            j = i + 1
            while 1:
                c = rawdata[j:j+1]

                if not c:
                    return -1
                if c.isspace():
                    j = j + 1
                else:
                    break
        else:
            j = i
        name, j = self._scan_name(j, declstartpos)
        if j < 0:
            return j
        while 1:

            c = self.rawdata[j:j+1]

            if not c:
                return -1
            if c in "'\"":
                m = _declstringlit_match(rawdata, j)
                if m:
                    j = m.end()
                else:

                    return -1    # incomplete

            elif c == ">":
                return j + 1
            else:
                name, j = self._scan_name(j, declstartpos)
                if j < 0:
                    return j

    # Internal -- scan a name token and the new position and the token, or
    # return -1 if we've reached the end of the buffer.
    def _scan_name(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        if i == n:
            return None, -1
        m = _declname_match(rawdata, i)
        if m:
            s = m.group()
            name = s.strip()
            if (i + len(s)) == n:
                return None, -1  # end of buffer
            return name.lower(), m.end()
        else:
            self.updatepos(declstartpos, i)
            raise AssertionError(

                "expected name token at %r" % rawdata[declstartpos:declstartpos+20]

            )

    # To be overridden -- handlers for unknown objects
    def unknown_decl(self, data):
        pass

    # Overridable -- finish processing of start+end tag: <tag.../>

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    # Overridable -- finish processing of start+end tag: <tag.../>
    def handle_tempstatestartendtag(self, tag, attrs):
        self.handle_tempstatestarttag(tag, attrs)
        self.handle_tempstateendtag(tag)


    # Overridable -- handle start tag
    def handle_starttag(self, tag, attrs):
        pass

    # Overridable -- handle template statement start tag
    def handle_tempstatestarttag(self, tag, attrs):
        pass

    # Overridable -- handle end tag

    def handle_endtag(self, tag):
        pass

    # Overridable -- handle template statement end tag
    def handle_tempstateendtag(self, tag):

        pass

    # Overridable -- handle character reference
    def handle_charref(self, name):
        pass

    # Overridable -- handle entity reference
    def handle_entityref(self, name):
        pass

    # Overridable -- handle data
    def handle_data(self, data):
        pass

    # Overridable -- handle comment

    def handle_comment(self, data):
        # need to add comment types for
        # other template languages

        pass

    # Overridable -- handle declaration
    def handle_decl(self, decl):
        pass

    # Overridable -- handle processing instruction
    def handle_pi(self, data):
        pass

    def unknown_decl(self, data):

        pass

