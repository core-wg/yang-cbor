all:  ietf-sid-file.yangtree
t: csv-to-sid-diff
e: ietf-system-from-csv.sid

ietf-sid-file.yangtree: ietf-sid-file.yang
	pyang ${PYANGPATH} -f tree --tree-print-structures --tree-line-length=70  ietf-sid-file.yang  > ietf-sid-file.yangtree

# please install the correct version of PYANG
# pip install git+https://github.com/core-wg/pyang.git@choice-case
.PHONY: pyang-sid
pyang-sid: ietf-system.yang
	git checkout c95b9ca29665c9d1d4704edf59efe54a14a4a417 ./ietf-system.sid
	# should work with python installed using pip, not pipx
	# if you installed pyang using pipx, you may fallback to simply:
	#  $ pyang --sid-update-fiel ietf-system.sid ietf-system.yang
	python -m pyang --sid-update-file ietf-system.sid ietf-system.yang
	cp ietf-system@2014-08-06.sid ietf-system.sid

# gem install sid-csv to get the tool

ietf-system.csv: ietf-system.sid
	sid-csv -tcsv $< >$@.new
	mv $@.new $@

csv-to-sid-diff: ietf-system.csv
	sid-csv -fcsv $< | diff ietf-system.sid -

ietf-system-from-csv.sid: ietf-system.csv
	sid-csv -fcsv $< >$@.new
	mv $@.new $@
