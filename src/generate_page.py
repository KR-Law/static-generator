from genericpath import isfile
import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        s = line.lstrip()
        if s.startswith("# "):
            title = s[2:].strip()
            if title == "":
                raise Exception("h1 title is empty")
            return title
    raise Exception("No title found")

def read_file(path):
    try:
        with open(path, "r") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error; the file {path} is not found.")
    except PermissionError:
        print(f"Error: You do not have permission to read {path}")
    except IOError as e:
        print(f"An unexpected I/O error occurred while reading: {e}")

def write_file(path, content):
    try:
        with open(path, "w") as file:
            file.write(content)
    except PermissionError:
        print(f"Error: You do not have permission to read {path}")
    except IOError as e:
        print(f"An unexpected I/O error occurred while reading: {e}")


def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.
    
    This function reads a markdown file, converts it to HTML, extracts the title,
    and inserts both the title and content into a template to generate a complete
    HTML page. The resulting page is written to the specified destination path.
    
    Args:
        from_path (str): Path to the source markdown file to be converted.
        template_path (str): Path to the HTML template file containing placeholders
                        for title and content.
        dest_path (str): Path where the generated HTML page will be saved.
                        Parent directories will be created if they don't exist.
    
    Returns:
        None
    
    Note:
        The template file should contain the placeholders "{{ Title }}" and 
        "{{ Content }}" which will be replaced with the extracted title and 
        converted HTML content respectively.
        
        Requires the following helper functions:
        - read_file(): to read file contents
        - markdown_to_html_node(): to convert markdown to HTML node
        - extract_title(): to extract title from markdown
        - write_file(): to write content to file
    """

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = read_file(from_path)
    template = read_file(template_path)
    node = markdown_to_html_node(markdown)
    content = node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", content)
    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
    write_file(dest_path, template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"Analyzing {dir_path_content}")
    if os.path.isfile(dir_path_content):
        if dir_path_content.lower().endswith(".md"):
            html_name = os.path.splitext(os.path.basename(dir_path_content))[0] + ".html"
            print(f"Calling generate page on {src} to {html_name}")
            generate_page(dir_path_content, template_path, html_name)
        return

    # it's a directory
    os.makedirs(dest_dir_path, exist_ok=True)

    for name in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, name)
        if os.path.isdir(src):
            generate_pages_recursive(src, template_path, os.path.join(dest_dir_path, name))
        elif src.lower().endswith(".md"):
            print("isdir")
            html_name = os.path.splitext(os.path.basename(src))[0] + ".html"
            dest_path = os.path.join(dest_dir_path, html_name)
            print(f"Calling generate page on {src} to {dest_path}")
            generate_page(src, template_path, dest_path)
