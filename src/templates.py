import os

def load_template(template_name):
    """Load a template from the templates directory."""
    template_path = os.path.join("templates", template_name)
    with open(template_path, "r", encoding="utf-8") as file:
        return file.read()