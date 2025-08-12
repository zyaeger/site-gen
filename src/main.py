import sys

from src import page_gen

STATIC_PATH = "./static"
PUBLIC_PATH = "./public"
DOCS_PATH = "./docs"
CONTENT_PATH = "./content"
TEMPLATE_PATH = "./template.html"


def main():
    basepath = "/"
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]

    print("Copying static files to docs directory...")
    page_gen.copy_dir(STATIC_PATH, DOCS_PATH)

    print("Generating content...")
    page_gen.generate_pages_recursive(CONTENT_PATH, TEMPLATE_PATH, DOCS_PATH, basepath)
    print("Done!")


if __name__ == "__main__":
    main()
