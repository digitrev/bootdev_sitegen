"""Main file, currently used for testing"""

import os
import shutil

from textnode import markdown_to_blocks, markdown_to_html_node


def main():
    """Main function, does the work"""
    copy_source_to_dest("static", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    generate_pages_recursive("content", "template.html", "public")


def copy_source_to_dest(source: str, destination: str, logging=False):
    """clear destination and copy files from source to destination"""
    if not os.path.exists(source):
        raise FileNotFoundError(f"Could not find folder: {source}")

    if os.path.exists(destination):
        if logging:
            print(f"Removing: {destination}")
        shutil.rmtree(destination)

    if logging:
        print(f"Creating folder: {destination}")
    os.mkdir(destination)

    for file_or_folder in os.listdir(source):
        new_source = os.path.join(source, file_or_folder)
        new_destination = os.path.join(destination, file_or_folder)
        if os.path.isfile(new_source):
            if logging:
                print(f"Copying: {new_source} to {new_destination}")
            shutil.copy(new_source, new_destination)
        elif os.path.isdir(new_source):
            copy_source_to_dest(new_source, new_destination)


def extract_title(markdown):
    """Extract h1 tag from markdown"""
    for block in markdown_to_blocks(markdown):
        if block.startswith("# "):
            return block.lstrip("#").strip()
    raise ValueError("Markdown requires h1 tag")


def generate_page(from_path, template_path, dest_path):
    """Generate page using template to destination"""
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    parent_dir = os.path.dirname(dest_path)
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)

    with open(from_path, encoding="utf-8") as file:
        markdown = file.read()
    with open(template_path, encoding="utf-8") as file:
        template = file.read()
    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(template)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    """Generates pages recurisvely"""
    for file in os.listdir(dir_path_content):
        source_file_path = os.path.join(dir_path_content, file)
        filename, ext = os.path.splitext(file)
        if ext.lower() == ".md":
            dest_file_path = os.path.join(dest_dir_path, f"{filename}.html")
            generate_page(source_file_path, template_path, dest_file_path)
        elif os.path.isdir(source_file_path):
            generate_pages_recursive(
                source_file_path, template_path, os.path.join(dest_dir_path, filename)
            )


main()
