import textwrap


def pretty_list(l, sep='\n'):
    return sep.join(l)


def ellipcise(text):
    return textwrap.shorten(text, width=1024, placeholder="...")


markdown_map = [
    {'tag': ['<i>', '</i>'], 'markdown': '*'},
    {'tag': ['<b>', '</b>'], 'markdown': '**'},
    {'tag': '<br>', 'markdown': '\n\n'}

]


def convert_to_markdown(text, replace_map):
    for replacement in replace_map:
        tag = replacement['tag']
        markdown = replacement['markdown']

        if isinstance(tag, list):
            for t in tag:
                text = text.replace(t, markdown)
        elif isinstance(tag, str):
            text = text.replace(tag, markdown)
        else:
            raise TypeError(
                f"tag must be of type 'list' or 'str', was {type(tag)}")

    return text


def markdownify(text):
    return convert_to_markdown(text, markdown_map)
