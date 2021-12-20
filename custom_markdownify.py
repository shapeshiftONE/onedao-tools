from markdownify import MarkdownConverter

# Extend Markdownify with a Custom MarkdownConverter to override certain features
class CustomerMarkDownConverter(MarkdownConverter):
    # Two newlines after images for spacing
    def convert_img(self, el, text, convert_as_inline):
        return super().convert_img(el, text, convert_as_inline) + '\n\n'

    # Do not replace <br/>'s
    def convert_br(self, el, text, convert_as_inline):
        return str(el)
    
    # Leave iframes as is (without their former container)
    def convert_iframe(self, el, text, convert_as_inline):
        return str(el) + "\n\n"

# Shorthand to use the custom markdownify class.
def custom_markdownify(html, **options):
    return CustomerMarkDownConverter(**options).convert(html)