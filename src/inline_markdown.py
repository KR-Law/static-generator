from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_node = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_node.append(node)
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("invalid Markdown: Delimiter was not closed.")
        for index in range(0, len(split_text)):
            if index % 2 == 0:
                if split_text[index] == "":
                    continue
                new_node.append(TextNode(split_text[index], TextType.TEXT))
            else:
                new_node.append(TextNode(split_text[index], text_type))
    return new_node