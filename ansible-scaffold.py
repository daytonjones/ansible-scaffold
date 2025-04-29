#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ansible Scaffold

Creates a clean, starter Ansible scaffold structure with roles, inventories, playbooks,
ansible.cfg, ssh.config, and .gitignore.

Supports optional automation flags for scripting and clean CLI output.

Author: Dayton Jones 
        https://pypi.org/user/daytonjones/
        https://github.com/daytonjones

License: MIT License
©2025 Dayton Jones
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import sys
import argparse
from pathlib import Path
import re
from colorama import init, Fore, Style

# --- Version ---
__version__ = "1.0.0"

# --- Initialize colorama
init(autoreset=True)

# --- Default contents for files ---

ANSIBLE_CFG_CONTENT = """\
[defaults]
bin_ansible_callbacks = True
callback_whitelist = timer
command_warnings = False
conditional_bare_variables = False
deprecation_warnings = False
display_skipped_hosts = False
fact_caching = jsonfile
fact_caching_connection = ./facts_cache
force_color = True
force_valid_group_names = ignore
forks = 10
gathering = smart
host_key_checking = False
interpreter_python=auto_silent
inventory = inventory
playbook_dir = playbooks
retry_files_enabled = False
roles_path = roles
stdout_callback = yaml
timeout = 30
transport = ssh

[inventory]
enable_plugins=yaml,host_list, script, auto, ini, toml
ignore_extensions=.pyc, .pyo, .swp, .bak, ~, .rpm, .md, .txt, .rst, .orig, .ini, .cfg, .retry

[inventory_plugins]
use_extra_vars=True

[inventory_plugin_yaml]
yaml_valid_extensions=.yaml, .yml, .json

[ssh_connection]
control_path = %(directory)s/%%h-%%r
pipelining = True
retries = 2
scp_if_ssh = True
ssh_args = -F ssh.config

[privilege_escalation]
become = true
become_method = sudo
become_ask_pass = false
"""

SSH_CFG_CONTENT = """\
Host *
  ForwardAgent yes
  ServerAliveInterval 300
  PreferredAuthentications publickey
  StrictHostKeyChecking no
  UserKnownHostsFile /dev/null
"""

GITIGNORE_CONTENT = """\
# Ansible
*.retry
*.orig
*.bak
*.log
*.tmp
*.swp
*.pyc
*.pyo
__pycache__/
facts_cache/
vault_pass.txt
.ssh-config
*.tar.gz
secrets.yml
*.vault
vault/
group_vars/*.vault
host_vars/*.vault
.env
venv/
.cache/
.idea/
.vscode/
"""

EMPTY_YAML_CONTENT = "---\n# empty\n"

# --- Helper Functions ---

def sanitize_name(name: str) -> str:
    """Sanitize user input for safe filenames (lowercase, underscores, remove special chars)."""
    name = name.strip().lower().replace(" ", "_")
    name = re.sub(r'[^a-zA-Z0-9_\-]', '', name)
    return name

def sanitize_playbook_name(name: str) -> str:
    """Sanitize playbook name, removing .yml/.yaml extension."""
    name = name.strip()
    name = re.sub(r'\.ya?ml$', '', name, flags=re.IGNORECASE)
    return sanitize_name(name)

def print_project_tree(base_path: Path):
    """Print a correct pretty tree of created files and directories."""
    print(f"\n{Fore.GREEN}📂 Project Structure:{Style.RESET_ALL}")
    print(f"{Style.BRIGHT}{base_path.name}/{Style.RESET_ALL}")

    for root, dirs, files in os.walk(base_path):
        rel_path = Path(root).relative_to(base_path)
        level = len(rel_path.parts)
        indent = "    " * level

        if root != str(base_path):
            print(f"{indent}{Fore.CYAN}📁 {Path(root).name}{Style.RESET_ALL}")

        subindent = "    " * (level + 1)
        for f in sorted(files):
            print(f"{subindent}{Fore.WHITE}📄 {f}{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}✅ Done!{Style.RESET_ALL}")

def print_help():
    """Print a custom, colorized help message."""
    print(f"""{Fore.CYAN}
Ansible Scaffold - Create a starter Ansible scaffold structure easily.

{Fore.YELLOW}Usage:{Style.RESET_ALL}
  ansible-scaffold [OPTIONS] [PATH]

{Fore.YELLOW}Options:{Style.RESET_ALL}
  -r, --role ROLE             Specify a role to create. Can be given multiple times.
  -d, --default-playbook NAME Name of the default playbook to create.
  -f, --force                 Force creation even if the path already exists.
  -n, --no-prompt             Don't prompt interactively (useful for automation).
  -t, --no-tree               Skip printing the project tree after creation.
  -h, --help                  Show this help message and exit.
  -v, --version               Show program version and exit.

{Fore.YELLOW}Examples:{Style.RESET_ALL}
  Create a new scaffold interactively:
    {Fore.GREEN}ansible-scaffold ~/my_ansible_project{Style.RESET_ALL}

  Create a scaffold with roles and a playbook automatically:
    {Fore.GREEN}ansible-scaffold ~/my_ansible_project -r webserver -r database -d site --force --no-prompt{Style.RESET_ALL}

{Fore.MAGENTA}Author:{Style.RESET_ALL} Dayton Jones
{Fore.MAGENTA}Links:{Style.RESET_ALL} https://pypi.org/user/daytonjones/ | https://github.com/daytonjones

{Fore.YELLOW}License:{Style.RESET_ALL} MIT License
""")

# --- Main Functions ---

def create_ansible_structure(base_path: Path):
    """Create the base Ansible project directory structure and starter files."""
    print(f"\n{Fore.GREEN}📁 Creating Ansible scaffold at: {base_path}{Style.RESET_ALL}\n")

    dirs = [
        base_path / "inventory" / "group_vars" / "all",
        base_path / "inventory" / "host_vars" / "all",
        base_path / "inventory" / "hosts",
        base_path / "roles",
        base_path / "playbooks",
        base_path / "facts_cache",
    ]

    files = {
        base_path / "ansible.cfg": ANSIBLE_CFG_CONTENT,
        base_path / "ssh.config": SSH_CFG_CONTENT,
        base_path / ".gitignore": GITIGNORE_CONTENT,
        base_path / "inventory" / "group_vars" / "all" / "main.yml": EMPTY_YAML_CONTENT,
        base_path / "inventory" / "host_vars" / "all" / "main.yml": EMPTY_YAML_CONTENT,
        base_path / "inventory" / "hosts" / "main.yml": EMPTY_YAML_CONTENT,
    }

    for directory in dirs:
        print(f"{Fore.CYAN}📂 Creating directory: {directory}{Style.RESET_ALL}")
        directory.mkdir(parents=True, exist_ok=True)

    for filepath, content in files.items():
        print(f"{Fore.WHITE}📄 Creating file: {filepath}{Style.RESET_ALL}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)

    print(f"\n{Fore.GREEN}✅ Ansible scaffold created successfully!{Style.RESET_ALL}")

def create_ansible_role(roles_base_path: Path, role_name: str):
    """Create a standard Ansible role with subfolders and starter files."""
    safe_role_name = sanitize_name(role_name)
    print(f"\n🛠 Creating role '{safe_role_name}' inside {roles_base_path}\n")

    role_path = roles_base_path / safe_role_name
    dirs = [
        role_path / "defaults",
        role_path / "files",
        role_path / "handlers",
        role_path / "meta",
        role_path / "tasks",
        role_path / "templates",
        role_path / "tests",
        role_path / "vars",
    ]

    files = {
        role_path / "defaults" / "main.yml": "---\n# defaults for {}\n".format(safe_role_name),
        role_path / "handlers" / "main.yml": "---\n# handlers for {}\n".format(safe_role_name),
        role_path / "meta" / "main.yml": "---\n# meta for {}\n".format(safe_role_name),
        role_path / "tasks" / "main.yml": f"""\
---
- name: Say hello from {safe_role_name}
  debug:
    msg: "Hello from the {safe_role_name} role!"
""",
        role_path / "vars" / "main.yml": "---\n# vars for {}\n".format(safe_role_name),
        role_path / "tests" / "inventory": "---\n# inventory placeholder\n",
        role_path / "tests" / "test.yml": "---\n# test playbook for {}\n".format(safe_role_name),
    }

    for directory in dirs:
        print(f"{Fore.CYAN}📂 Creating directory: {directory}{Style.RESET_ALL}")
        directory.mkdir(parents=True, exist_ok=True)

    for filepath, content in files.items():
        print(f"{Fore.WHITE}📄 Creating file: {filepath}{Style.RESET_ALL}")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(content)

    print(f"\n{Fore.GREEN}✅ Role '{safe_role_name}' created successfully!{Style.RESET_ALL}\n")

def create_default_playbook(playbooks_path: Path, playbook_name: str, roles_list=None):
    """Create a properly formatted starter playbook referencing given roles."""
    safe_name = sanitize_playbook_name(playbook_name)
    playbook_file = playbooks_path / f"{safe_name}.yml"

    if roles_list:
        roles_entries = "\n".join([f"    - {sanitize_name(role)}" for role in roles_list])
    else:
        roles_entries = "    - sample_role"

    content = f"""\
---
- name: {playbook_name}
  hosts: all
  gather_facts: true

  roles:
{roles_entries}
"""

    print(f"\n{Fore.WHITE}📄 Creating default playbook: {playbook_file}{Style.RESET_ALL}")
    playbook_file.parent.mkdir(parents=True, exist_ok=True)
    with open(playbook_file, "w") as f:
        f.write(content)

    print(f"{Fore.GREEN}✅ Default playbook '{playbook_name}' created at {playbook_file}{Style.RESET_ALL}")

def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("path", nargs="?", help="Destination path where the scaffold will be created.")
    parser.add_argument("-r", "--role", action="append", help="Specify a role to create. Can be given multiple times.")
    parser.add_argument("-d", "--default-playbook", help="Name of default playbook to create.")
    parser.add_argument("-f", "--force", action="store_true", help="Force creation even if path exists.")
    parser.add_argument("-n", "--no-prompt", action="store_true", help="Don't prompt interactively.")
    parser.add_argument("-t", "--no-tree", action="store_true", help="Skip printing the project tree.")
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit.")
    parser.add_argument("-v", "--version", action="store_true", help="Show program version and exit.")

    args = parser.parse_args()

    if args.help:
        print_help()
        sys.exit(0)

    if args.version:
        print(f"{Fore.CYAN}Ansible Scaffold version {__version__}{Style.RESET_ALL}")
        sys.exit(0)

    return args

def interactive_prompt():
    """Prompt user for project path interactively."""
    print(f"{Fore.CYAN}📦 Welcome to Ansible Scaffold!{Style.RESET_ALL}\n")
    path = input(f"{Fore.CYAN}Enter the full path to create your scaffold: {Style.RESET_ALL}").strip()
    if not path:
        print(f"{Fore.RED}⚠️ No path entered. Exiting.{Style.RESET_ALL}")
        sys.exit(1)
    return path

def confirm_overwrite(path: Path, force: bool):
    """Confirm overwriting an existing directory unless forced."""
    if path.exists() and not force:
        response = input(f"{Fore.YELLOW}⚠️ WARNING: Path {path} already exists. Continue? (y/N): {Style.RESET_ALL}").strip().lower()
        if response != "y":
            print(f"{Fore.RED}❌ Operation cancelled.{Style.RESET_ALL}")
            sys.exit(0)

def prompt_for_role_creation(base_path: Path):
    """Prompt user to optionally create a starter role."""
    answer = input(f"{Fore.CYAN}➕ Would you like to create a starter role? (y/N): {Style.RESET_ALL}").strip().lower()
    if answer == "y":
        role_name = input(f"{Fore.CYAN}📝 Enter role name: {Style.RESET_ALL}").strip()
        if role_name:
            create_ansible_role(base_path / "roles", role_name)
        else:
            print(f"{Fore.YELLOW}⚠️ No role name provided. Skipping role creation.{Style.RESET_ALL}")

def main():
    """Main CLI entry point."""
    args = parse_args()

    if args.path:
        project_path = Path(args.path).expanduser().resolve()
    else:
        project_path = Path(interactive_prompt()).expanduser().resolve()

    confirm_overwrite(project_path, args.force)
    create_ansible_structure(project_path)

    if args.role:
        for role in args.role:
            create_ansible_role(project_path / "roles", role)
    elif not args.no_prompt:
        prompt_for_role_creation(project_path)
    else:
        print(f"{Fore.YELLOW}ℹ️ Skipping role creation (--no-prompt specified){Style.RESET_ALL}")

    if args.default_playbook:
        create_default_playbook(project_path / "playbooks", args.default_playbook, args.role)

    if not args.no_tree:
        print_project_tree(project_path)

if __name__ == "__main__":
    os.system("clear")
    main()
