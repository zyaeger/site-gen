import sys

from src import page_gen

STATIC_PATH = "./static"
PUBLIC_PATH = "./docs"
CONTENT_PATH = "./content"
TEMPLATE_PATH = "./template.html"
DEFAULT_BASEPATH = "/"


def main():
    basepath = DEFAULT_BASEPATH
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Copying static files to docs directory...")
    page_gen.copy_dir(STATIC_PATH, PUBLIC_PATH)

    print("Generating content...")
    page_gen.generate_pages_recursive(
        CONTENT_PATH, TEMPLATE_PATH, PUBLIC_PATH, basepath
    )
    print("Done!")


if __name__ == "__main__":
    main()
