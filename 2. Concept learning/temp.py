#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
"""
Created on Tue Oct 18 18:00:18 2016

@author: meo
"""

# subprogram that parses a single line (describing a single example) read from the dataset file
# and returns a pair of values (boolean target, list of strings) where the boolean target is TRUE is the class attribute value is '+'
# each string of the list is a literal of an hypothesis or a value assignment to an attribute
def parse_fields(line):
	fields= line.split(',')
	literal_list = [(f.rstrip()).lstrip() for f in fields] # eliminate leading and trailing spaces with list comprehension
   
	target_fields = literal_list[0].split('=')
	return [target_fields[1]=='+', literal_list[1:]]

# subprogram that reads the dataset and returns a list of pairs (target,description) where each element of the list describes one example
def load_dataset(filename):
	file=open(filename, "r")
	result = []
	for line in file: # reads the file line by line
		target, description = parse_fields(line)
		# result is a dictionary of two key-value pairs (target_key: target_value, description_key: description_value) 
		# where each element of the pair is a key:value pair.
		# the first element of the pair has a key 'target' whose value is a boolean that is TRUE is the class of the example is positive, FALSE otherwise
		# the second element of the pair has a key 'description'; the value is a list containing strings corresponding to literals (a value assignment to an attribute)
		result.append({'target': target, 'description': description })
	file.close()   
	return result

# The program takes as input (as the first parameter of the command line) the filename of the dataset
# it reads the dataset (by means of load_dataset subprogram)
# and updates one of the two borders of the version space (lgg and lub) as soon a new example comes in
# if the example is positive it updates the lgg (by subprogram lgg_conj)
# if the example is negative it updates the lub (by subprogram mg_consistent)
	
'''
Most-specific hypothesis or least-general generalization, called S.
Aggiorna incrementalmente l'ipotesi con ogni esempio positivo, generalizzando
l'ipotesi il minimo necessario per soddisfare il nuovo esempio.

Most-general consistent hypothesis, called G.

LUB: copre solo gli esempi positivi e non quelli negativi.
	Least sta a dire: il minimo set di attributi possibili.
	
GLB: copre solo gli esempi positivi e non quelli negativi. 
	Great sta per massimo numero di attributi possibili.

'''
def main():
	filename=sys.argv[1]
	lgg = [] # list of hypothesis valid for the lower border of the version space
	lub = [] # list of hypothesis valid for the upper border of the version space
	data = load_dataset(filename) # reads the dataset
	
	# Tengo data come copia di backup. Lavoro su data2
	data2 = data
	
	# Prendo i valori del primo esempio e li inserisco in lgg.
	# Serve come inizializzazione per il calcolo di lgg.
	# Il primo elemento della lista lgg è il primo esempio positivo.
	for value in data2[0]['description']:
		if data2[0]['target'] == True:
			lgg.append(value)
	
	# Elimino il primo elemento dal dataset perché l'ho già considerato.
	del data2[0]
	
	# Loopo in data2 alla ricerca degli elementi positivi da aggiungere al lgg.
	for example in data2:
		if example['target'] == True:
			lgg = lgg_conj(lgg, example['description'])
	
	# Stampo lgg appena calcolato.
	print("LGG: ", lgg)
	
	# Inizializzo lub ad lgg.
	# Il lub finché non si verificano esempi negativi è TRUE, cioè la
	# massima generalizzazione dello spazio delle ipotesi.
	# Quando compaiono esempi negativi, si specializza il meno possibile il lub
	# tale da rimanere completo e consistente.
	# Adesso si aggiorna il lub e lo inizializzo ad lgg, sicuro che sia
	# completo e si va a rimuovere da questo lub le clausole che comprono 
	# esempi negativi.
	lub = lgg
	# Loopo alla ricerca di elementi negativi per aggiornare il lub.
	for example in data2: # loop on each example in data
		if example['target'] == False:
			lub = mg_consistent(lub, example['description'])
	
	print("LUB: ", lub)

# H è l'ipotesi allo stato attuale, x è il concetto corrente.
def lgg_conj(H, x):
	z = []
	fields = []
	for value in x:
		fields.append(value)
	z = list(set(H).intersection(fields))
	return z

def mg_consistent(H, x):
	# Lista risultato finale.
	z = []
	# Lista di appoggio necessaria ad estrarre le clausole del concetto 
	# corrente.
	fields = []
	# Aggiungo le clausole di x in fields.
	for value in x:
		fields.append(value)
	# Controllo se ci sono clausole in H che attualmente comprono l'esempio
	# negativo x.
	# Se non ci sono, allora vuol dire che l'ipotesi H va bene come lub.
	if len(covers(H, fields)) == 0:
		return H
	# Se invece l'ipotesi attuale copre uno delle clausole contenute nel 
	# concetto corrente x, allora elimino dall'ipotesi attuale H la clausola 
	# coperta del concetto negativo.
	z = list(set(H).difference(covers(H, fields)))
	return z

def covers(list1, list2):
    result = []
    for element in list1:
        if element in list2:
            result.append(element)
    return result

main()