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
def main():
   filename=sys.argv[1]
   lgg=[] # list of hypothesis valid for the lower border of the version space
   lub =[] # list of hypothesis valid for the upper border of the version space
   data = load_dataset(filename) # reads the dataset

   for example in data: # loop on each example in data
      print(example['target'])
      print(example['description'])

main()
