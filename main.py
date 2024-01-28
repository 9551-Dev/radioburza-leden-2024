import os
import configparser
import shutil

def check_file_exists(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return False
    return True

def check_folder_exists(folder_path):
    if not os.path.exists(folder_path):
        print(f"Error: Folder not found: {folder_path}")
        return False
    return True

def read_config():
    print("Reading configuration...")
    config = configparser.ConfigParser()
    config.read('cfg.ini')

    title        = config.get('Settings', 'title')
    image_folder = config.get('Settings', 'image_folder')

    template_path = config.get('Core', 'template_path')
    css_path      = config.get('Core', 'css_path')
    js_path       = config.get('Core', 'js_path')

    output_folder         = config.get('Output', 'output_folder')
    images_directory_name = config.get('Output', 'images_directory_name')
    core_directory_name   = config.get('Output', 'core_directory_name')
    output_file_name      = config.get('Output', 'output_file_name')

    if not check_folder_exists(image_folder):
        print("Exiting: Image folder not found.")
        exit(1)
    if not (check_file_exists(template_path) and check_file_exists(css_path) and check_file_exists(js_path)):
        print("Exiting: One or more core files not found.")
        exit(1)

    print("Configuration read successfully.")
    return title, image_folder, template_path, css_path, js_path, output_folder, images_directory_name, core_directory_name, output_file_name

def get_image_filenames(image_folder):
    print(f"Scanning image folder: {image_folder}")
    image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    print(f"Found {len(image_files)} image(s):")
    for image_file in image_files:
        print(f" - {image_file}")
    return sorted(image_files)

def generate_html(title, image_folder, template_path, css_path, js_path, output_folder, images_directory_name, core_directory_name, output_file_name):
    print("\nGenerating HTML...")
    with open(template_path, 'r') as template_file:
        template_content = template_file.read()
    with open(js_path, 'r') as js_file:
        js_content = js_file.read()
    with open(css_path, 'r') as css_file:
        css_content = css_file.read()

    image_files = get_image_filenames(image_folder)
    image_paths = [os.path.join(images_directory_name, os.path.basename(image_file)) for image_file in image_files]

    output_images_folder = os.path.join(output_folder, images_directory_name)
    os.makedirs(output_images_folder, exist_ok=True)

    for image_file, image_path in zip(image_files, image_paths):
        print(f"Copying image: {image_file} to {output_images_folder}")
        shutil.copy(os.path.join(image_folder, image_file), output_images_folder)

    copied_image_paths = [f'"{path}"' for path in image_paths]
    image_tags         = '\n'.join([f'        <img src={path} alt="{os.path.basename(path)}" onclick=\'open_image_viewer({path})\'>'
                                    for path in copied_image_paths])

    template_content = template_content.replace('{{title}}', title)
    template_content = template_content.replace('{{css_path}}', os.path.join(core_directory_name, os.path.basename(css_path)))
    template_content = template_content.replace('{{js_path}}', os.path.join(core_directory_name, os.path.basename(js_path)))
    template_content = template_content.replace('{{image_tags}}', image_tags)

    image_paths_js = ",\n    ".join(copied_image_paths)
    js_content     = js_content.replace('{{image_paths}}', image_paths_js)

    output_core_folder = os.path.join(output_folder, core_directory_name)
    os.makedirs(output_core_folder, exist_ok=True)

    output_js_path = os.path.join(output_core_folder, os.path.basename(js_path))
    with open(output_js_path, 'w') as output_js_file:
        output_js_file.write(js_content)

    output_css_path = os.path.join(output_core_folder, os.path.basename(css_path))
    with open(output_css_path, 'w') as output_css_file:
        output_css_file.write(css_content)

    output_file_path = os.path.join(output_folder, output_file_name)
    with open(output_file_path, 'w') as output_file:
        output_file.write(template_content)

    print(f'Generated {output_file_path} successfully.')

if __name__ == '__main__':
    title, image_folder, template_path, css_path, js_path, output_folder, images_directory_name, core_directory_name, output_file_name = read_config()

    print(f'\nTitle: {title}')
    print(f'Image Folder: {image_folder}')
    print(f'Template Path: {template_path}')
    print(f'CSS Path: {css_path}')
    print(f'JS Path: {js_path}')
    print(f'Output Folder: {output_folder}')
    print(f'Images Directory Name: {images_directory_name}')
    print(f'Core Directory Name: {core_directory_name}')
    print(f'Output File Name: {output_file_name}')

    generate_html(title, image_folder, template_path, css_path, js_path, output_folder, images_directory_name, core_directory_name, output_file_name)
