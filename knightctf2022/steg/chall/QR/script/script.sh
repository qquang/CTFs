#!/bin/bash

# Requires imagemagic and zbarimg

flag=$(for i in {0..48}
do
        zbarimg QR_Code_From_The_Future-$i.jpg | grep "QR" | cut -d ":" -f 2
done)
#Removes extra space from the flag and writes the flag to file name living_qr_code_flag
echo $flag | tr -d ' ' >> living_qr_code_flag
#Cleans up all those newfiles that were created by imagemagick
