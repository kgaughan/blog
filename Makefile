PY?=python
PELICAN?=pelican

PORT:=8000

INPUTDIR=${PWD}/content
OUTPUTDIR=${PWD}/output
CONFFILE=${PWD}/pelicanconf.py
PUBLISHCONF=${PWD}/publishconf.py

SSH_HOST=cian.talideon.com
SSH_USER=freebsd
SSH_TARGET_DIR=/home/$(SSH_USER)/sites/canthack.it/web

help:
	@echo 'Makefile for a pelican Web site'
	@echo
	@echo 'Usage:'
	@echo '   make html                   (re)generate the web site'
	@echo '   make clean                  remove the generated files'
	@echo '   make regenerate             regenerate files upon modification'
	@echo '   make publish                generate using production settings'
	@echo '   make serve [PORT=8000]      serve site at http://localhost:8000'
	@echo '   make devserver [PORT=8000]  start/restart develop_server.sh'
	@echo '   make stopserver             stop local server'
	@echo '   make ssh_deploy             deploy the web site via SSH'
	@echo '   make rsync_deploy           deploy the web site via rsync+ssh'
	@echo '   make copy_deploy            deploy the web site via rsync+ssh'
	@echo '   make copy_deploy            deploy the web site by copying locally'
	@echo '   make drafts                 list draft posts'
	@echo '   make categories             list categories alphabetically'

drafts:
	@grep -rl '^:status: *draft$$' $(INPUTDIR)

categories:
	@find $(INPUTDIR) -name \*.rst -exec sed -n -E 's/^:category: *(.*)/\1/p' {} \; | sort -u

html:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE)

clean:
	rm -rf $(OUTPUTDIR)

regenerate:
	$(PELICAN) -r $(INPUTDIR) -o $(OUTPUTDIR) -s $(CONFFILE)

serve:
	cd $(OUTPUTDIR) && $(PY) -m pelican.server $(PORT)

devserver:
	${PWD}/develop_server.sh restart $(PORT)

stopserver:
	${PWD}/develop_server.sh stop
	@echo 'Stopped Pelican and SimpleHTTPServer processes running in background.'

publish:
	$(PELICAN) $(INPUTDIR) -o $(OUTPUTDIR) -s $(PUBLISHCONF)

ssh_deploy: publish
	scp -P $(SSH_PORT) -r $(OUTPUTDIR)/* $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR)

rsync_deploy: publish
	rsync -P -rvc --delete $(OUTPUTDIR)/ $(SSH_USER)@$(SSH_HOST):$(SSH_TARGET_DIR) --cvs-exclude

copy_deploy: publish
	cp -r $(OUTPUTDIR)/* $(SSH_TARGET_DIR)

.PHONY: html help clean regenerate serve devserver publish
.PHONY: ssh_deploy rsync_deploy copy_deploy
.PHONY: drafts categories
