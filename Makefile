TMP := $(shell mktemp -d)
FILES := index.html

update:
	python dl_all.py
	python build_trees.py
	cd ../lichess-user-data/ && \
		git commit -a -m "update user data" && \
		git push

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
