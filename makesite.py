import os
import markdown
from jinja2 import Environment, FileSystemLoader

# Path to your Obsidian vault
obsidian_vault_path = './'
# Path where you want to save the generated HTML files
output_path = './ghpages'
# Path to the templates directory
template_path = './jinjatemplates'

def convert_markdown_to_html(markdown_content):
    """Converts markdown content to HTML."""
    html_content = markdown.markdown(markdown_content)
    return html_content

def save_html_file(html_content, output_file_path):
    """Saves HTML content to a file."""
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def generate_link_structure(vault_path, output_path):
    """Generates a nested dictionary structure for links."""
    link_structure = {}
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                relative_path = os.path.relpath(root, vault_path)
                link_path = os.path.join(relative_path, os.path.splitext(file)[0] + '.html')
                
                parts = link_path.split(os.sep)
                current_level = link_structure
                for part in parts:
                    if part not in current_level:
                        current_level[part] = {}
                    current_level = current_level[part]
                current_level['__link__'] = os.path.join(relative_path, os.path.splitext(file)[0] + '.html').replace('\\', '/')
    
    print("Generated Link Structure:")
    print(link_structure)
    return link_structure

def generate_index_page(link_structure, output_path, template_env):
    """Generates the index page with links."""
    template = template_env.get_template('index.html')

    html_content = template.render(links=link_structure, description="Welcome to my site! Here you'll find links to various pages.")

    output_file_path = os.path.join(output_path, 'index.html')
    save_html_file(html_content, output_file_path)

def process_markdown_files(vault_path, output_path, template_env):
    """Processes all markdown files in the given directory."""
    for root, _, files in os.walk(vault_path):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    markdown_content = f.read()

                # Convert to HTML
                html_content = convert_markdown_to_html(markdown_content)

                # Determine output file path
                relative_path = os.path.relpath(file_path, vault_path)
                output_file_path = os.path.join(output_path, os.path.splitext(relative_path)[0] + '.html')

                # Ensure the output directory exists
                os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

                # Save HTML file
                save_html_file(html_content, output_file_path)

    # Generate the index page
    link_structure = generate_link_structure(vault_path, output_path)
    generate_index_page(link_structure, output_path, template_env)

if __name__ == '__main__':
    # Set up Jinja2 template environment
    env = Environment(loader=FileSystemLoader(template_path))

    process_markdown_files(obsidian_vault_path, output_path, env)
