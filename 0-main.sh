#!/bin/sh
rm -rf file.json;
rm -rf dev/file.json;

echo 'create State name="Arizona"' | python3 console.py ;
echo 'create State name="California"' | python3 console.py ;
echo 'create State name="Louisiana"' |  python3 console.py ;
echo 'create State name="Texas"' | python3 console.py ;

