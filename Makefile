all:
	# chrpath package must be installed to build
	python3 -m nuitka --show-progress --follow-imports --standalone andromeda.py
	mv andromeda.dist andromeda-linux
	cp -r assets/ andromeda-linux/
	cp README andromeda-linux/

zip:
	zip -r andromeda-linux.zip andromeda-linux/
	sha1sum andromeda-linux.zip > andromeda-linux.zip.sha1

test:
	chmod +x runtests.sh
	./runtests.sh

clean:
	rm -rf andromeda.dist/
	rm -rf andromeda.build/
	rm -rf andromeda-linux/
	rm -f andromeda-linux.zip
	rm -f andromeda-linux.zip.sha1
