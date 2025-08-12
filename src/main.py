from src import page_gen

STATIC_PATH = "./static"
PUBLIC_PATH = "./public"
CONTENT_PATH = "./content"
TEMPLATE_PATH = "./template.html"


def main():
    print("Copying static files to public directory...")
    page_gen.copy_dir(STATIC_PATH, PUBLIC_PATH)

    print("Generating content...")
    page_gen.generate_pages_recursive(CONTENT_PATH, TEMPLATE_PATH, PUBLIC_PATH)
    print("Done!")


if __name__ == "__main__":
    main()
