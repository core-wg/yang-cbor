all:  ietf-sid-file.yangtree
t: csv-to-sid-diff
e: ietf-system-from-csv.sid

ietf-sid-file.yangtree: ietf-sid-file.yang
	pyang ${PYANGPATH} -f tree --tree-print-structures --tree-line-length=70  ietf-sid-file.yang  > ietf-sid-file.yangtree

# gem install sid-csv to get the tool

ietf-system.csv: ietf-system.sid
	sid-csv -tcsv $< >$@.new
	mv $@.new $@

csv-to-sid-diff: ietf-system.csv
	sid-csv -fcsv $< | diff ietf-system.sid -

ietf-system-from-csv.sid: ietf-system.csv
	sid-csv -fcsv $< >$@.new
	mv $@.new $@
