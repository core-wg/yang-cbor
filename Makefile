include lib/main.mk
$(warning CI_IS_PR $(CI_IS_PR))
$(warning IS_MASTER $(IS_MASTER))
$(warning CI $(CI))
$(warning TRAVIS_PULL_REQUEST //$(TRAVIS_PULL_REQUEST)//)
$(warning CI_PULL_REQUESTS //$(CI_PULL_REQUESTS)//)

lib/main.mk:
	git submodule update --init

