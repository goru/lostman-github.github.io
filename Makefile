html:
	pelican pelican/content/ -o . -s pelican/pelicanconf.py

server:
	python3 -m pelican.server

clean:
	rm -rf author categories.html feeds tag theme archives.html authors.html category index.html posts tags.html
	rm -rf pelican/__pycache__ pelican/cache pelican/output
