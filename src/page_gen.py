import os

from src.block_markdown import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]

    raise ValueError("Provided Markdown does not contain h1 header")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as md_f:
        md = md_f.read()

    with open(template_path, "r", encoding="utf-8") as tf:
        template = tf.read()

    html_string = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as w_f:
        w_f.write(html)
