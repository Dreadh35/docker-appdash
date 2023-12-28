# list_labels.py
import docker
import os
import requests

APPDASH_LABEL_PREFIX = "org.appdash.app."

def download_logo(url, app_name):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        logo_filename = f"logo/{app_name}.{url.split('.')[-1]}"
        with open(logo_filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        return logo_filename
    return None

def generate_html_page():
    client = docker.from_env()
    containers = client.containers.list(all=True)

    grouped_labels = {}

    for container in containers:
        container_labels = container.labels
        container_name = container.name

        print(f"Container: {container_name}")

        if container_labels:
            for key, value in container_labels.items():
                # Remove extra double-quote characters from the label value
                value = value.strip('"')

                if key.endswith((".port", ".logo", ".name")) and key.startswith(APPDASH_LABEL_PREFIX):
                    # Remove the prefix and split the string at "."
                    parts = key[len(APPDASH_LABEL_PREFIX):-4].split(".")
                    if parts:
                        app_name = parts[0]
                        if app_name not in grouped_labels:
                            grouped_labels[app_name] = {"port": "", "logo": "", "name": ""}
                        if key.endswith(".port"):
                            grouped_labels[app_name]["port"] = value
                        elif key.endswith(".logo"):
                            grouped_labels[app_name]["logo"] = value
                        elif key.endswith(".name"):
                            grouped_labels[app_name]["name"] = value

    # Create the "logo" folder if it doesn't exist
    os.makedirs("logo", exist_ok=True)

    # Generate HTML content from the template
    template_filename = "template.html"
    with open(template_filename, "r") as template_file:
        template_content = template_file.read()

    # Generate content for the template
    html_content = ""
    for app_name, app_info in grouped_labels.items():
        logo_url = app_info['logo']
        logo_path = download_logo(logo_url, app_name)  # Download the logo and get the path
        name_label = app_info.get('name', 'No Name')  # Use 'No Name' if 'name' label is not present

        if logo_path:
            html_content += f"<div class='app-entry'>"
            html_content += f"<a href='javascript:void(0)' onclick='navigateToApp({app_info['port']})'>"
            html_content += f"<img class='app-logo' src='{logo_path}' alt='{name_label}' title='{name_label}'>"
            html_content += f"<div>{name_label}</div></a></div>"
        else:
            # Placeholder for missing logo
            html_content += f"<div class='app-entry'>"
            html_content += f"<a href='javascript:void(0)' onclick='navigateToApp({app_info['port']})'>"
            html_content += f"<div>{name_label}</div></a></div>"

    # Replace the placeholder in the template with the generated content
    template_content = template_content.replace("{content}", html_content)

    # Write HTML content to a file named index.html
    with open("index.html", "w") as html_file:
        html_file.write(template_content)

if __name__ == "__main__":
    generate_html_page()
    # Start a simple Python web server to serve the HTML page
    os.system("python -m http.server 8000")
