$(warning CI_IS_PR $(CI_IS_PR))
$(warning IS_MASTER $(IS_MASTER))
$(warning CI $(CI))
include lib/main.mk

lib/main.mk:
	git submodule update --init
