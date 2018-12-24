OBJ=	static/css/pygments.css \
	static/css/style.css

css: $(OBJ)

clean:
	rm -f $(OBJ)

develop: .venv
	.venv/bin/pip install pyscss pygments

.venv:
	python3 -m venv .venv

static/css/style.css: static/scss/style.scss
	.venv/bin/python -mscss $? --output=$@

static/css/pygments.css:
	.venv/bin/pygmentize -f html -S default > $@

.PHONY: css clean develop
