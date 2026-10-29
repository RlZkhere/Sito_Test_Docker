#!/bin/bash
conta=0
while true
do
controllo_selenium=$(ps -a | grep chrom | grep -v grep | wc -l)
sleep 10
conta=$((conta+1))
if [ $controllo_selenium -eq 0 ] #SE SELENIUM NON E PIU ATTIVO CON CHROMIUM ALLORA RITORNA TRUE
then
exit 0
fi
if [ $conta -gt 7200 ] #SE PASSANO PIU DI 20 ORE ESCE CON FALSE
then
exit 1
fi
done
