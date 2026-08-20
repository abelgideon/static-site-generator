import os
import shutil

from block_markdown import markdown_to_html_node


def main():
    if os.path.exists("public/"):
        shutil.rmtree("public/")

    os.mkdir("public")

    copy_src_to_dest("static", "public")

    generate_page("content/index.md", "template.html", "public/index.html")


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


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as f:
        from_content = f.read()

    with open(template_path) as f:
        template_content = f.read()

    html = markdown_to_html_node(from_content).to_html()
    title = extract_title(from_content)

    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        _ = f.write(template_content)


if __name__ == "__main__":
    main()
