
import argparse
import src.main.Baguette as BG
from jinja2 import Environment, PackageLoader, select_autoescape, BaseLoader, TemplateNotFound
from os.path import join, exists, getmtime

# TODO: Define stopword list in the BAGUETTE class

class TemplateLoader(BaseLoader):
    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        print("Environment: ", environment)
        print("Template: ", template)
        path = join(self.path, template)
        if not exists(path):
            raise TemplateNotFound(path)
        mtime = getmtime(path)
        with open(path) as f:
            source = f.read()
        return source, path, lambda: mtime == getmtime(path)




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument("files", nargs='+')

    args = parser.parse_args()
    print(args.files[0])
    print(args.files[1])
    print(args.files[2])

    baguette = BG.Baguette()
    tf_idf = baguette.process_files(args.files, idf=True, k=10)

    env = Environment(
        loader=TemplateLoader("src/templates"),
        autoescape=select_autoescape()
    )
    data = tf_idf.to_dict()
    template = env.get_template("world_cloud.html")

    with open("output.html", "w") as f:
        f.write(template.render(words=data["TF-IDF"]))
