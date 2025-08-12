import os
import shutil


STATIC_PATH = "./static"
PUBLIC_PATH = "./public"


def main():
    print("Copying static files to public directory...")
    copy_dir("./static", "./public")
    print("Done!")


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


if __name__ == "__main__":
    main()
