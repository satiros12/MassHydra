rm -r dist/
rm ./*.exe
for f in *.py; do pyinstaller -F $f;  done
for f in dist/*.exe; do cp $f .; done
for f in *.exe; do cp $f Attacker/.; done
