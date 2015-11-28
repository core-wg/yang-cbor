include lib/main.mk
$(warning CI_IS_PR $(CI_IS_PR))
$(warning IS_MASTER $(IS_MASTER))
$(warning CI $(CI))

lib/main.mk:
	git submodule update --init
