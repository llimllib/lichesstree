TMP := $(shell mktemp -d)
FILES := index.html

.PHONY: publish
publish:
	git clone --depth 1 `git config --get remote.origin.url` ${TMP}
	cd ${TMP} && \
	  git branch -D gh-pages; \
	  git push origin :gh-pages; \
	  git checkout --orphan gh-pages
	cp -r ${FILES} ${TMP}
	cd ${TMP} && \
	  git add ${FILES} && \
	  git commit -m "publish script" && \
	  git push -f -u origin gh-pages

# https://github.com/cortesi/devd
.PHONY: serve
serve:
	devd -o -w index.html /=. /lichess-user-data/=../lichess-user-data
