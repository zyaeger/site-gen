import os
import shutil
from pathlib import Path

from src.block_markdown import markdown_to_html_node


def copy_dir(src_dir: str, dest_dir: str) -> None:
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        print(f" * {src_path} -> {dest_path}")
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_dir(src_path, dest_path)


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]

    raise ValueError("Provided Markdown does not contain h1 header")


def generate_page(
    from_path: str, template_path: str, dest_path: str, basepath: str
) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r", encoding="utf-8") as md_f:
        md = md_f.read()

    with open(template_path, "r", encoding="utf-8") as tf:
        template = tf.read()

    html_string = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as w_f:
        w_f.write(html)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
) -> None:
    contents = os.listdir(dir_path_content)
    for item in contents:
        next_path_content = os.path.join(dir_path_content, item)
        next_dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(next_path_content):
            next_dest_path = Path(next_dest_path).with_suffix(".html")
            generate_page(next_path_content, template_path, next_dest_path, basepath)
        else:
            # print(f"Moving to next dir: {next_path_content}, {next_dest_path}")
            generate_pages_recursive(
                next_path_content, template_path, next_dest_path, basepath
            )
