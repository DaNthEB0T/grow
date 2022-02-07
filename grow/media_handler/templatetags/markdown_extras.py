from django import template
from django.template.defaultfilters import stringfilter
from io import StringIO
import markdown as md

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['nl2br'])

def unmark_element(element, stream=None):
    if stream is None:
        stream = StringIO()
    if element.text:
        stream.write(element.text)
    for sub in element:
        unmark_element(sub, stream)
    if element.tail:
        stream.write(element.tail)
    return stream.getvalue()

md.Markdown.output_formats["plain"] = unmark_element
__md = md.Markdown(output_format="plain")
__md.stripTopLevelTags = False

def unmark(text):
    return __md.convert(text)