import argparse
from midi_reader.pymidi import get_pitch
from os import listdir
from os.path import isfile, join

import json

from db.DbController import MsqlController
from datetime import datetime
import traceback

stJosengTable = [
	{'idx': 0, 'name': "C", 'rank': ['A', 'B', 'C', 'D', 'E', 'F', 'G']},
	{'idx': 1, 'name': "C#", 'rank': ['A#', 'C', 'C#', 'D#', 'F', 'F#', 'G#']},
	{'idx': 2, 'name': "D", 'rank': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G']},
	{'idx': 3, 'name': "Eb", 'rank': ['A#', 'C', 'D', 'D#', 'F', 'G', 'G#']},
	{'idx': 4, 'name': "E", 'rank': ['A', 'B', 'C#', 'D#', 'E', 'F#', 'G#']},
	{'idx': 5, 'name': "F", 'rank': ['A', 'A#', 'C', 'D', 'E', 'F', 'G']},
	{'idx': 6, 'name': "F#", 'rank': ['A#', 'B', 'C#', 'D', 'F', 'F#', 'G#']},
	{'idx': 7, 'name': "G", 'rank': ['A', 'B', 'C', 'D', 'E', 'F#', 'G']},
	{'idx': 8, 'name': "Ab", 'rank': ['A#', 'C', 'C#', 'D#', 'F', 'G', 'G#']},
	{'idx': 9, 'name': "A", 'rank': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#']},
	{'idx': 10, 'name': "Bb", 'rank': ['A', 'A#', 'C', 'D', 'D#', 'F', 'G']},
	{'idx': 11, 'name': "B", 'rank': ['A#', 'B', 'C#', 'D#', 'E', 'F#', 'G#']},
	{'idx': 12, 'name': "c", 'rank': ['B', 'C', 'D', 'D#', 'F', 'G', 'G#']},
	{'idx': 13, 'name': "c#", 'rank': ['A', 'C', 'C#', 'D#', 'E', 'F#', 'G#']},
	{'idx': 14, 'name': "d", 'rank': ['A', 'A#', 'C#', 'D', 'E', 'F', 'G']},
	{'idx': 15, 'name': "d#", 'rank': ['A#', 'B', 'D', 'D#', 'F', 'F#', 'G#']},
	{'idx': 16, 'name': "e", 'rank': ['A', 'B', 'C', 'D#', 'E', 'F#', 'G']},
	{'idx': 17, 'name': "f", 'rank': ['A#', 'C', 'C#', 'E', 'F', 'G', 'G#']},
	{'idx': 18, 'name': "f#", 'rank': ['A', 'B', 'C#', 'D', 'F', 'F#', 'G#']},
	{'idx': 19, 'name': "g", 'rank': ['A', 'A#', 'C', 'D', 'D#', 'F#', 'G']},
	{'idx': 20, 'name': "g#", 'rank': ['A#', 'B', 'C#', 'D#', 'E', 'G', 'G#']},
	{'idx': 21, 'name': "a", 'rank': ['A', 'B', 'C', 'D', 'E', 'F', 'G#']},
	{'idx': 22, 'name': "a#", 'rank': ['A', 'A#', 'C', 'C#', 'D#', 'F', 'F#']},
	{'idx': 23, 'name': "b", 'rank': ['A#', 'B', 'C#', 'D', 'E', 'F#', 'G']}]


class CMusic():
	def __init__(self):
		pass

	def getJoseng(self, in_filename):
		score = []
		save_cnt = 0
		save_rank = 1
		save_ary = -1

		stReadTable = [{'name': "A", 'cnt': 0, 'rank': 0},
					   {'name': "A#", 'cnt': 0, 'rank': 0},
					   {'name': "B", 'cnt': 0, 'rank': 0},
					   {'name': "C", 'cnt': 0, 'rank': 0},
					   {'name': "C#", 'cnt': 0, 'rank': 0},
					   {'name': "D", 'cnt': 0, 'rank': 0},
					   {'name': "D#", 'cnt': 0, 'rank': 0},
					   {'name': "E", 'cnt': 0, 'rank': 0},
					   {'name': "F", 'cnt': 0, 'rank': 0},
					   {'name': "F#", 'cnt': 0, 'rank': 0},
					   {'name': "G", 'cnt': 0, 'rank': 0},
					   {'name': "G#", 'cnt': 0, 'rank': 0}]

		reads = get_pitch(in_filename)

		for read in reads:
			readname = read['note']
			score.append(readname)
			for i in range(0, 12):
				if stReadTable[i]['name'] == readname:
					stReadTable[i]['cnt'] = stReadTable[i]['cnt'] + 1
					break

		for i in range(0, 9):
			for j in range(0, 12):
				if stReadTable[j]['rank'] != 0:
					continue

				if stReadTable[j]['cnt'] > save_cnt:
					save_cnt = stReadTable[j]['cnt']
					save_ary = j

			if save_ary != -1:
				stReadTable[save_ary]['rank'] = save_rank
				save_rank = save_rank + 1
				save_ary = -1
				save_cnt = 0
		cmpstr = []

		for read in stReadTable:
			if read['rank'] == 8:
				save_cnt8 = read['cnt']
			elif read['rank'] != 0:
				cmpstr.append(read['name'])
				if read['rank'] == 7:
					save_cnt = read['cnt']

		# print(stReadTable)
		# print(cmpstr)
		for stJoseng in stJosengTable:
			intersection = list(set(stJoseng['rank']) & set(cmpstr))
			eq = len(intersection)
			stJoseng['eq'] = eq

		select = sorted(stJosengTable, key=lambda x: x['eq'], reverse=True)
		# print(select[0]['rank'])
		ton = select[0]['name']
		return ton, cmpstr, stReadTable, score


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='python Implementation')
	parser.add_argument('--dir', type=str, default='', help='input_dir')
	args = parser.parse_args()

	dir = args.dir
	print(dir)

	# flist = [f for f in listdir(dir) if isfile(join(dir, f))]
	cm = CMusic()

	ton, cmpstr, stReadTable, score = cm.getJoseng(in_filename='009count.mid')
	print(ton, cmpstr, stReadTable, score)
	print(len(score))
	print(len(stReadTable))

	# for item in flist:
	# 	file_path = join(dir, item)
	# 	# print(file_path)
	#
	# 	music_name =item.rsplit('.', 1)[0]
	#
	# 	ton, rank, read_table = cm.getJoseng(in_filename=file_path)
	# 	rank = json.dumps(rank)
	# 	read_table = json.dumps(read_table)
	# 	print(item, music_name, ton, rank, read_table)
	#
	# 	yyyymmdd = datetime.today().strftime('%Y-%m-%d')
	# 	hhmmss = datetime.today().strftime('%H:%M:%S')
