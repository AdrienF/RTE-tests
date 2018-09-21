import json
import numpy as np
import matplotlib.pyplot as plt


def buildUnitsDict(actual_generation_per_unit_json):
	"""
	Build correspondance tables btween unit names and EIC code from a actual_generations_per_unit json file
	:param actual_generation_per_unit_file: json files
	:return: two dictionnaries eic_code:name and name:eic_code
	"""
	units = [d['unit'] for d in actual_generation_per_unit_json['actual_generations_per_unit']]
	eic_code_dict={}
	unit_name_dict={}
	for unit in units:
		eic_code_dict[unit['eic_code']] = unit['name']
		unit_name_dict[unit['name']] = unit['eic_code']
	return eic_code_dict, unit_name_dict

def plotProductionForUnit(actual_generation_per_unit_json, eic_codes):
	"""
	Plot production for units corresponding to eic_codes
	:param actual_generation_per_unit_json: json data
	:param eic_code: list of eic_codes for production units
	:return:
	"""
	units_data = [d['values'] for d in actual_generation_per_unit_json['actual_generations_per_unit'] if d['unit']['eic_code'] in eic_codes]
	for i, eic in enumerate(eic_codes):
		xlabels = [d['end_date'] for d in units_data[i]]
		values = [d['value'] for d in units_data[i]]
		plt.plot(values, label=str(eic))
	plt.xticks(np.arange(len(xlabels)), xlabels, rotation=80)
	# Tweak spacing to prevent clipping of tick-labels
	plt.subplots_adjust(bottom=.5)
	plt.legend()
	plt.show()
	return 0


if __name__ == '__main__':

	with open('ActualGenerationPerUnit.json', 'r') as infile:
		data = json.load(infile)

		eic_code_dict, unit_name_dict = buildUnitsDict(data)
		# print('{} production units : '.format(len(unit_name_dict), [k+'\n' for k in unit_name_dict]))
		# for k in unit_name_dict.keys():
		# 	print('  ' + k + ' : ' + unit_name_dict[k])

		plotProductionForUnit(data, [unit_name_dict['TRICASTIN 1'], unit_name_dict['TRICASTIN 2'], unit_name_dict['TRICASTIN 3'], unit_name_dict['TRICASTIN 4']])