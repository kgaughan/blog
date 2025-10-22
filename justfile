ssh_user := "keith"
ssh_host := "lir.talideon.com"
ssh_target_dir := "/usr/local/www/keith.gaughan.ie/web"

[private]
default:
	@just --list

# List draft posts
[group("Introspection")]
drafts:
	@grep -Eril '^:?status: *draft$' content || echo None

# List categories alphabetically
[group("Introspection")]
categories:
	@find content \( -name \*.rst -o -name \*.md \) -exec sed -n -E 's/^(:c|C)ategory: *(.*)/\2/p' {} \; | sed 's/, /\n/g' | sort -u

# Remove any generated files
[group("Maintenance")]
clean:
	@test -e output && find output -mindepth 1 -delete

[private]
build cfg:
	@uv run pelican content -o output -s {{cfg}}

# (Re)generate the website with local settings
[group("Build")]
html: (build "pelicanconf.py")

# Serve the site at http://localhost:8000
[group("Testing")]
serve: html
	@cd output && uv run -m http.server --bind 127.0.0.1

# Start/restart the development server
[group("Testing")]
devserver: html
	@./develop_server.sh restart

# Generate using production settings
[group("Build")]
publish: (build "publishconf.py")

# Upload website via rsync+ssh
[group("Deployment")]
upload: publish
	@rsync -P -rvczz --delete --exclude=.DS_Store --exclude='.*.sw?' --cvs-exclude output/ "{{ssh_user}}@{{ssh_host}}:{{ssh_target_dir}}"

# Initially configure the site with Ansible
[group("Deployment")]
deploy:
	@ansible-playbook deploy.yml -i hosts.ini --diff
