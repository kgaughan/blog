PELICAN=pelican
PELICANOPTS=

BASEDIR:=$(PWD)
INPUTDIR:=$(BASEDIR)/content
OUTPUTDIR:=$(BASEDIR)/output
CONFFILE:=$(BASEDIR)/pelicanconf.py
PUBLISHCONF:=$(BASEDIR)/publishconf.py

SSH_HOST:=lir.talideon.com
SSH_USER:=keith
SSH_TARGET_DIR:=/usr/local/www/keith.gaughan.ie/web

help:
	@echo 'Makefile for a pelican Web site'
	@echo
	@echo 'Usage:'
	@echo '   make html                   (re)generate the web site'
	@echo '   make clean                  remove the generated files'
	@echo '   make publish                generate using production settings'
	@echo '   make serve [PORT=8000]      serve site at http://localhost:8000'
	@echo '   make devserver [PORT=8000]  start/restart develop_server.sh'
	@echo '   make upload                 upload the web site via rsync+ssh'
	@echo '   make drafts                 list draft posts'
	@echo '   make categories             list categories alphabetically'
	@echo '   make deploy                 initially deploy the site'

drafts:
	@egrep -ril '^:?status: *draft$$' $(INPUTDIR) || echo None

categories:
	@find $(INPUTDIR) \( -name \*.rst -o -name \*.md \) -exec sed -n -E 's/^(:c|C)ategory: *(.*)/\2/p' {} \; | sed 's/, /\n/g' | sort -u

html: clean $(OUTPUTDIR)/index.html
	@echo 'Done'

$(OUTPUTDIR)/%.html:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE) $(PELICANOPTS)

clean:
	test -e $(OUTPUTDIR) && find $(OUTPUTDIR) -mindepth 1 -delete || :

serve:
	cd $(OUTPUTDIR) && python3 -m http.server --bind 127.0.0.1 

devserver:
	$(BASEDIR)/develop_server.sh restart

publish:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF) $(PELICANOPTS)

upload: publish
	rsync -P -rvczz --delete --exclude=.DS_Store --exclude='.*.sw?' --cvs-exclude $(OUTPUTDIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)

deploy:
	ansible-playbook deploy.yml -i hosts.ini --diff

.PHONY: html help clean regenerate serve devserver publish upload
.PHONY: drafts categories deploy
