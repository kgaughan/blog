Title: Bootstrapping development VMs with Ansible
Date: 2019-03-08 16:42
Category: Systems Administration
Status: published

I often need VMs set up locally for development purposes. Setting these up manually can be time-consuming and error-prone, so I use [Ansible](https://www.ansible.com/) to almost entirely automate the process.

There are two problems that need to be solved when initially doing something like this: (a)  a minimal bootstrap that makes the VM useful for ongoing maintenance, and (b) the subsequent maintenance of the VM. I'll be covering the first part in this post.

I'm using VMWare Fusion currently and will be setting up Cent OS 7, but these steps largely generalise across any Unix-like operating system.

## Initial setup

Spin up a minimal install of your operating system, creating _just_ a root user and ensuring that networking is configured, giving it some kind of unique name. I like to name my local VMs after [SpongeBob SquarePants](https://en.wikipedia.org/wiki/SpongeBob_SquarePants) characters, and I'll be referring to this one as _patrick_.

Now that your VM is spun up, you'll need to figure out what its current IP address is and create a [hosts file](https://docs.ansible.com/ansible/latest/user_guide/intro_inventory.html). Here's an example:

```ini
patrick.local ansible_host=192.168.149.146

[bootstrap]
patrick.local
```

Here, I'm using ``patrick.local``, the [mDNS](http://www.multicastdns.org/) name, as the VM will be advertised in the mDNS `.local` domain once mDNS is configured on it. You should replace _192.168.149.146_ with whatever your VM's current IP address is.

## The bootstrap role

Next we need to create a role for performing the initial bootstrap of the VM. This only needs to be done once, but it ought ot be idempotent.

Create the directory structure with:

```sh
mkdir -p roles/bootstrap/{handlers,tasks} group_vars
touch roles/bootstrap/{handlers,tasks}/main.yml group_vars/all
```

Open up ``roles/bootstrap/tasks/main.yml``, and add:

```yaml
- name: install essentials
  yum:
    name:
      - deltarpm
      - epel-release
    update_cache: true

- name: ensure the EPEL key is in place
  rpm_key:
    key: /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
```

This installs some very basic packages to get started:

* _deltarpm_ helps ensure we're only downloading the minimum we need to; and
* _epel-release_ ensures the [EPEL](https://fedoraproject.org/wiki/EPEL) YUM repo is available to use, as I make heavy use of it.

To make EPEL useful, we need to ensure its key is installed.

We can then upgrade all the installed packages to the latest versions:
```yaml
- name: upgrade installed packages
  yum:
    name: '*'
    state: latest
  notify:
    - reboot
    - remove old kernels
```

Notice the two handlers mentioned at the end? Those do some cleanup at the end, and should go into ``roles/bootstrap/handlers/main.yml``:
```yaml
- name: reboot
  reboot:

- name: remove old kernels
  command: "/usr/bin/package-cleanup --oldkernels --count=2 -y"
```

The the first does a reboot of the machine if any of the packages were upgraded, and the second cleans out any older kernels, ensuring that there's always at least one older kernel present, so that if the latest kernel has issues, you can alway boot into an older one that's known to work.

We can now install some basic packages to make the VM useful:
```yaml
- name: install basic tools
  yum:
    name:
      - fish
      - nss-mdns
      - open-vm-tools
      - sudo
```

* [_fish_](https://fishshell.com/) is my preferred shell, so if you don't use that, choose something that better suits your tastes.
* _nss-mdns_ installs the [Name Service Switch](https://en.wikipedia.org/wiki/Name_Service_Switch) module for Multicast DNS, as well as the [Avahi](https://www.avahi.org/) daemon. Doing so will ensure we can address the VM by name subsequently, rather than having to know its IP address.
* [_open-vm-tools_](https://github.com/vmware/open-vm-tools) is a set of tools for integrating with VMWare. If you use some other solution, there's bound to be an equivalent. I install this, as I like to include a shared directory for exchanging files between the host and the VM.
* And finally, _sudo_, which will come in useful after we've bootstrapped everything.

While Avahi will advertise itself initially, after a while, it will stop. To allow access after the VM has been running for a while, you'll need to open the firewall up to multicast DNS traffic:
```yaml
- name: open the firewall for avahi
  firewalld:
    zone: public
    permanent: true
    service: mdns
    state: enabled
```

If you were happy running everything as root, you could stop here, but that's not a great idea. Instead, let's create a user:
```yaml
- name: create a user
  user:
    name: "{{ username }}"
    comment: "{{ full_name }}"
    groups: wheel
    shell: "{{ shell }}"
    state: present
    generate_ssh_key: "{{ key_name is undefined }}"
  register: user

- name: make .ssh directory for the user
  file:
    path: "{{ user.home }}/.ssh"
    state: directory
    owner: "{{ username }}"
    group: "{{ username }}"
    mode: '600'
```

You'll notice several variables defined here. Let's add them to ``group_vars/all``:
```yaml
username: charlie
full_name: Charlie User
shell: /usr/bin/fish
key_name: id_ed25519
```

Most of these are obvious, but ``key_name`` is special. It refers to what you call your main key on your workstation, as you might need to copy it into the VM if you're using it to access services over SSH and are only able to provide a single key. If this isn't an issue for you, you can leave this out.

We also create ``~/.ssh`` for the new user.

If ``key_name`` is defined, then we copy it into ``~/.ssh`` in the VM:
```yaml
- name: copy up local ssh key
  copy:
    src: "{{ lookup('env', 'HOME') }}/.ssh/{{ item.name }}"
    dest: "{{ user.home }}/.ssh"
    owner: "{{ username }}"
    group: "{{ username }}"
    mode: "{{ item.mode }}"
  loop:
    - name: "{{ key_name }}"
      mode: "600"
    - name: "{{ key_name }}.pub"
      mode: "644"
  when: key_name is defined
```

I like to populate my ``~/.ssh/authorized_keys`` file from Github:
```yaml
- name: populate authorized_keys
  authorized_key:
    user: "{{ item }}"
    key: "https://github.com/{{ github_user }}.keys"
    state: present
  loop:
    - root
    - "{{ username }}"
  when: github_user is defined
```

For this, you'll need to have a setting in ``group_vars/all`` called ``github_user`` that gives your Github username.

Finally, just to make life easy, allow our user, which is a member of the _wheel_ group, to run commands with _sudo_ without any password prompt:
```yaml
- name: give sudo to wheel group
  lineinfile:
    path: /etc/sudoers
    line: "%wheel ALL=(ALL) NOPASSWD: ALL"
    validate: "visudo -cf %s"
```

Finally, ensure the VM runs in the One True Timezone:
```
- name: ensure timezone is UTC
  timezone:
    name: UTC
```

You'll need to create a small playbook to use the role now:
```yaml
---
- hosts: bootstrap
  remote_user: root
  gather_facts: false
  roles:
    - bootstrap
```

And then run it:
```sh
ansible-playbook -i hosts bootstrap.yml --ask-pass
```

You can now edit ``hosts``, removing the explicit IP address, as once your VM is running, it should be resolvable:
```ini
patrick.local

[bootstrap]
patrick.local
```
