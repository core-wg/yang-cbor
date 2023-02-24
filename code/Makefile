all:  ietf-sid-file.yangtree

ietf-sid-file.yangtree: ietf-sid-file.yang
	pyang ${PYANGPATH} -f tree --tree-print-structures --tree-line-length=70  ietf-sid-file.yang  > ietf-sid-file.yangtree

