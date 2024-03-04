# Assuming you are running this script from the root of the repository
import os
import shutil
import uuid


def copy_files():
    # Copy specified files from web_flask to web_dynamic
    source_folder = 'web_flask'
    destination_folder = 'web_dynamic'

    files_to_copy = ['static', 'templates/100-hbnb.html',
                     '__init__.py', '100-hbnb.py']

    for file_path in files_to_copy:
        source_path = os.path.join(source_folder, file_path)
        destination_path = os.path.join(destination_folder, file_path)
        shutil.copytree(source_path, destination_path)


def rename_files():
    # Rename 100-hbnb.py to 0-hbnb.py
    # Rename 100-hbnb.html to 0-hbnb.html
    os.rename('web_dynamic/100-hbnb.py', 'web_dynamic/0-hbnb.py')
    os.rename('web_dynamic/templates/100-hbnb.html',
              'web_dynamic/templates/0-hbnb.html')


def update_route():
    # Update 0-hbnb.py to replace the existing route to /0-hbnb/
    # If 100-hbnb.html is not present, use 8-hbnb.html instead
    file_path = 'web_dynamic/0-hbnb.py'
    with open(file_path, 'r') as file:
        content = file.read()
        content = content.replace('/0-hbnb/', '/')
        content = content.replace('100-hbnb.html', '8-hbnb.html')

    with open(file_path, 'w') as file:
        file.write(content)


def add_cache_id():
    # Add a variable cache_id to the render_template in 0-hbnb.py
    # The value of this variable must be a UUID (uuid.uuid4())
    file_path = 'web_dynamic/0-hbnb.py'
    with open(file_path, 'r') as file:
        content = file.read()
        content = content.replace(
            'render_template', 'render_template, cache_id=str(uuid.uuid4())')

    with open(file_path, 'w') as file:
        file.write(content)


def add_query_string():
    # In 0-hbnb.html, add cache_id as a query string to each <link> tag URL
    file_path = 'web_dynamic/templates/0-hbnb.html'
    with open(file_path, 'r') as file:
        content = file.read()
        content = content.replace(
            '<link', '<link href="../static/styles/4-common.css?{{ cache_id }}"')

    with open(file_path, 'w') as file:
        file.write(content)


if __name__ == '__main__':
    copy_files()
    rename_files()
    update_route()
    add_cache_id()
    add_query_string()
