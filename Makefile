TMP := $(shell mktemp -d)
FILES := index.html test_tree.json

.PHONY: publish
publish:
	git clone --depth 1 `git config --get remote.origin.url` ${TMP}
	# gh-pages might not exist, hence the ||
	cd ${TMP} && \
	  git branch -D gh-pages; \
	  git push origin :gh-pages; \
	  git checkout --orphan gh-pages
	cp ${FILES} ${TMP}
	cd ${TMP} && \
	  git add ${FILES} && \
	  git commit -m "publish script" && \
	  git push -f -u origin gh-pages
