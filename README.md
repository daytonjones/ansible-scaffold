# Ansible Scaffold

Create a clean, starter **Ansible scaffold** structure easily and quickly.

---

## 📈 Description

**Ansible Scaffold** is a lightweight CLI tool to instantly generate a fully organized Ansible project layout:

- Inventory directory with group_vars, host_vars, and hosts
- `ansible.cfg` file with sane defaults
- Starter `.gitignore`
- `ssh.config` ready for Ansible ssh_connection
- Roles structure with all subfolders (`tasks/`, `handlers/`, `defaults/`, etc)
- Playbooks directory
- Facts cache directory
- Optional default playbook creation

Perfect for automation, bootstrapping new environments, or kickstarting new projects.

---

## 🔄 Installation

```bash
pip install --user ansible-scaffold
```

Or clone and install locally:

```bash
git clone https://github.com/daytonjones/ansible-scaffold.git
cd ansible-scaffold
pip install --user -e .
```

---

## 🔄 Usage

```bash
ansible-scaffold [OPTIONS] [PATH]
```

If [PATH] is omitted, you will be prompted.

### Options:

| Option | Long | Description |
|:------:|:----:|:------------|
| `-r` | `--role ROLE` | Create a specific role (can be repeated) |
| `-d` | `--default-playbook NAME` | Create a default playbook with given name |
| `-f` | `--force` | Overwrite existing project directory without confirmation |
| `-n` | `--no-prompt` | Skip interactive prompts (fully automatic) |
| `-t` | `--no-tree` | Skip printing the generated project tree |
| `-h` | `--help` | Show this help message and exit |
| `-v` | `--version` | Show version and exit |

### Examples

Create an Ansible scaffold interactively:

```bash
ansible-scaffold ~/my_ansible_project
```

Create a scaffold with multiple roles and a starter playbook automatically:

```bash
ansible-scaffold ~/new_project -r webserver -r database -d site --force --no-prompt
```

---

## 👉 Features

- Fast and clean structure generation
- Default ansible.cfg with best practices
- Automatic starter playbook with role entries
- Colorized, friendly CLI prompts
- Safe overwrite behavior with `--force` option
- Full support for automation scripting

---

## 👉 License

MIT License

---

## 📢 Author

**Dayton Jones**  
✨ [PyPI Profile](https://pypi.org/user/daytonjones/)  ✨ [GitHub Profile](https://github.com/daytonjones)

---

## 💡 Todo / Future Plans

- Optional support for ansible-vault starter integration
- Project templates (for common layouts)
- Plugin-based architecture for customizations
