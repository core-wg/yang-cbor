include lib/main.mk
$(warning CI_IS_PR $(CI_IS_PR))
$(warning IS_MASTER $(IS_MASTER))
$(warning CI $(CI))
$(warning TRAVIS_PULL_REQUEST //$(TRAVIS_PULL_REQUEST)//)
$(warning CI_PULL_REQUESTS //$(CI_PULL_REQUESTS)//)
$(warning CI_REPO_FULL //$(CI_REPO_FULL)//)
$(warning CI_USER //$(CI_USER)//)
$(warning CI_REPO //$(CI_REPO)//)
$(warning TRAVIS_REPO_SLUG //$(TRAVIS_REPO_SLUG)//)

lib/main.mk:
	git submodule update --init

