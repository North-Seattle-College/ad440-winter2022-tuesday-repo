import json
import re 

global_list = []

# open json file 
with open('floop_data_15k.json', 'r', encoding='utf-8') as reader: 
      data = json.load(reader)

# regex for finding all sentences
pattern = re.compile('(?<![a-zA-Z0-9_]\.[a-zA-Z0-9_].)(?<![A-Z][a-z][0-9]\.)(?<=\.|\?)\s')

for element in data: 
      mini_list = re.split(pattern, element)
      for sentence in mini_list: 
            sentence = sentence.strip()
            global_list.append(sentence) 

print('\n'.join(map(str, global_list)))
