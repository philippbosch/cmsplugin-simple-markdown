from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django import forms
from django.utils.translation import ugettext_lazy as _
from cmsplugin_simple_markdown.models import SimpleMarkdownPlugin
from cms.utils.page_resolver import get_page_from_path
import re


class SimpleMarkdownCMSPluginForm(forms.ModelForm):
    class Meta:
        model = SimpleMarkdownPlugin
        widgets = {
            'markdown_text': forms.Textarea(attrs={'cols': 100, 'rows': 20, 'style': 'font-family: Monaco, monospace;'})
        }


class SimpleMarkdownCMSPlugin(CMSPluginBase):
    model = SimpleMarkdownPlugin
    name = _('Text (Markdown)')
    render_template = 'cmsplugin_simple_markdown/simple_markdown.html'
    admin_preview = False
    form = SimpleMarkdownCMSPluginForm

    def replace_links(self, markdown_text):
        def link_repl(match):
            page = get_page_from_path(match.group(1))
            if page:
                return "(" + page.get_absolute_url() + ")"
            else:
                return "(#" + match.group(1) + ")"

        return re.sub('\(page:([^\)]+)\)', link_repl, markdown_text)

    def render(self, context, instance, placeholder):
        context['text'] = self.replace_links(instance.markdown_text)
        return context

plugin_pool.register_plugin(SimpleMarkdownCMSPlugin)
