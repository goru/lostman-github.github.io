html:
	LC_ALL=en_US.UTF-8 pelican pelican/content/ -o . -s pelican/pelicanconf.py

serve:
	python3 -m pelican.server

clean:
	rm -rf author categories.html feeds tag theme archives.html authors.html category index.html posts tags.html
	rm -rf pelican/__pycache__ pelican/cache pelican/output
