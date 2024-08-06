import os
import shutil
import utils
import logging


logger = logging.getLogger()


def copy_recurse(src, dest):
    if not os.path.exists(src):
        logger.warning("file %s does not exist", src)
        return

    for file in os.listdir(src):
        src_new = os.path.join(src, file)
        dest_new = os.path.join(dest, file)

        if os.path.isdir(src_new):
            os.mkdir(dest_new)
            copy_recurse(src_new, dest_new)
        else:
            shutil.copy(src_new, dest_new)
            logger.info("copied file from %s to %s", src_new, dest_new)


def copy_content():
    cwd = os.getcwd()
    src = os.path.join(cwd, "static")
    dest = os.path.join(cwd, "public")
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    copy_recurse(src, dest)


def generate():
    cwd = os.getcwd()
    src = os.path.join(cwd, "content")
    tmpl = os.path.join(cwd, "template.html")
    dest = os.path.join(cwd, "public")
    generate_pages_recursively(src, tmpl, dest)


def generate_pages_recursively(src, tmpl, dest):
    if not os.path.exists(src):
        logger.warning("directory does not exist: %s", src)
        return

    for file in os.listdir(src):
        src_new = os.path.join(src, file)
        dest_new = os.path.join(dest, file)

        if os.path.isdir(src_new):
            os.mkdir(dest_new)
            generate_pages_recursively(src_new, tmpl, dest_new)
        else:
            dest_new = dest_new.replace(".md", ".html")
            utils.generate_page(src_new, tmpl, dest_new)


def main():
    logging.basicConfig(filename='ss-jenny_main.log', level=logging.INFO)
    copy_content()
    generate()


main()
