import os
import shutil
import sys
from pathlib import Path

from block_markdown import markdown_to_html_node


def main():
    basepath = sys.argv[1] if len(sys.argv) >= 2 else "/"

    if os.path.exists("docs/"):
        shutil.rmtree("docs/")

    os.mkdir("docs")

    copy_src_to_dest("static", "docs")

    generate_pages_recursive("content", "template.html", "docs", basepath)


def copy_src_to_dest(src: str, dest: str):
    for file in os.listdir(src):
        file_source = os.path.join(src, file)

        if os.path.isfile(file_source):
            file_dest = shutil.copy(file_source, os.path.join(dest, file))
            print(f"{file} copied from {file_source} to {file_dest}")

        else:
            os.mkdir(os.path.join(dest, file))
            copy_src_to_dest(file_source, os.path.join(dest, file))


def extract_title(markdown: str):
    lines = markdown.splitlines()
    first_line = lines[0].strip()

    if not first_line.startswith("# "):
        raise Exception("Title is missing")

    return first_line.removeprefix("# ").strip()


def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        from_content = f.read()

    with open(template_path) as f:
        template_content = f.read()

    html = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)

    template_content = template_content.replace('href="/', f'href="{basepath}')
    template_content = template_content.replace('src="/', f'src="{basepath}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        _ = f.write(template_content)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
):
    for file in os.listdir(dir_path_content):
        file_source = os.path.join(dir_path_content, file)

        if os.path.isfile(file_source):
            generate_page(
                dest_path=os.path.join(dest_dir_path, f"{Path(file_source).stem}.html"),
                from_path=file_source,
                template_path=template_path,
                basepath=basepath,
            )

        else:
            generate_pages_recursive(
                file_source, template_path, os.path.join(dest_dir_path, file), basepath
            )


if __name__ == "__main__":
    main()
