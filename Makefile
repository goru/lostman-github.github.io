html:
	LC_ALL=en_US.UTF-8 pelican pelican/content/ -o . -s pelican/pelicanconf.py

serve:
	python -m pelican.server

clean:
	git checkout archives.html author/ authors.html categories.html category/ feeds/ index*.html posts/ tag/ tags.html
	git clean -df category/ posts/ tag/
	rm -rf pelican/__pycache__ pelican/cache pelican/output
