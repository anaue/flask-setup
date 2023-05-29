#!/bin/bash
mv /start.sh /start.bkp.sh
cp /start-reload.sh /start.sh

mv ./prestart.sh ./prestart-done.sh
/start.sh