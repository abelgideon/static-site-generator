import os
import shutil


def main():
    if os.path.exists("public/"):
        shutil.rmtree("public/")

    os.mkdir("public")

    copy_src_to_dest("static", "public")


def copy_src_to_dest(src: str, dest: str):
    for file in os.listdir(src):
        file_source = os.path.join(src, file)

        if os.path.isfile(file_source):
            file_dest = shutil.copy(file_source, os.path.join(dest, file))
            print(f"{file} copied from {file_source} to {file_dest}")

        else:
            os.mkdir(os.path.join(dest, file))
            copy_src_to_dest(file_source, os.path.join(dest, file))


if __name__ == "__main__":
    main()
