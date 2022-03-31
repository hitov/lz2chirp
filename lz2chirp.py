#!/usr/bin/env python3
# encoding: utf-8

import argparse
import csv

# ./lz2chirp.py --input LZ_repeaters.csv --output lz_repeaters.csv --uhf --vhf

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='Input repeaters list')
parser.add_argument('--output', help='Output repeaters list')
parser.add_argument('--vhf', action='store_true', help='Add vhf bands')
parser.add_argument('--uhf', action='store_true', help='Add uhf bands')


args = parser.parse_args()

print("input = " + args.input)
print("vhf = " + str(args.vhf))
print("uhf = " + str(args.uhf))

categories = []

if args.vhf:
    categories.append('VHF')
if args.uhf:
    categories.append('UHF')

outputs = []
location = 1
with open(args.input, newline='', encoding='ISO-8859-1') as incsv:
    reader = csv.DictReader(incsv, delimiter='\t')
    for row in reader:
        category = row['category']
        callsign = row['repeater_callsign']
        rx = row['rx']
        tx = row['tx']
        ctcss = row['CTCSS']

        if not category in categories:
            continue

        output = {}
        output['Location'] = location
        output['Name'] = callsign
        output['Frequency'] = rx
        output['Duplex'] = 'split'
        output['Offset'] = tx
        output['Tone'] = 'Tone' if ctcss != '' else ''
        output['rToneFreq'] = ctcss if ctcss != '' else '88.5'
        output['cToneFreq'] = '88.5'
        output['DtcsCode'] = '23'
        output['DtcsPolarity'] = 'NN'
        output['Mode'] = 'FM'
        output['TStep'] = '5'
        output['Skip'] = ''
        output['Comment'] = ''
        output['URCALL'] = ''
        output['RPT1CALL'] = ''
        output['RPT2CALL'] = ''
        location += 1
        outputs.append(output)
        print(output)

with open(args.output, 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=outputs[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(outputs)