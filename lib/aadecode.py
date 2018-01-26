from __future__ import unicode_literals # turns everything to unicode
import re

class aadecode(object):

	vars_list = {}
	# The basic method for deobfuscating aaencoded javascript is outlined here:
	# https://stackoverflow.com/questions/8883999/how-do-these-javascript-obfuscators-generate-actual-working-code#answer-8885873
	# These are the variables 1 - 16 as on the link. I also make them into dictionary entries to avoid using eval
	#1
	ff9f03c9ff9fff89='undefined'
	vars_list.update({'ff9f03c9ff9fff89':'undefined'})
	#2
	o=ff9fff70ff9f=_=3
	vars_list.update({'o':o})
	vars_list.update({'ff9fff70ff9f':ff9fff70ff9f})
	vars_list.update({'_':_})
	#3
	c=ff9f0398ff9f=ff9fff70ff9f-ff9fff70ff9f
	vars_list.update({'ff9f0398ff9f':ff9f0398ff9f})
	vars_list.update({'c':c})
	#4
	ff9f0414ff9f = ff9f0398ff9f = o^_^o/ o^_^o
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	vars_list.update({'ff9f0398ff9f':ff9f0398ff9f})
	#5
	ff9f0414ff9f={'ff9f0398ff9f': '_' ,
					'ff9f03c9ff9fff89' : (str(ff9f03c9ff9fff89==3) + '_')[ff9f0398ff9f] ,
					'ff9fff70ff9fff89' : (str(ff9f03c9ff9fff89) + '_')[o^_^o - ff9f0398ff9f] ,
					'ff9f0414ff9fff89': (str(ff9fff70ff9f==3) +'_')[ff9fff70ff9f] }
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#6
	ff9f0414ff9f [ff9f0398ff9f] = (str(ff9f03c9ff9fff89==3) +'_') [c^_^o];
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#7
	ff9f0414ff9f ['c'] = "[object Object]" [ ff9fff70ff9f+ff9fff70ff9f-ff9f0398ff9f ]
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#8
	ff9f0414ff9f ['o'] = "[object Object]" [ff9f0398ff9f];
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#9
	ff9foff9f=ff9f0414ff9f ['c'] + ff9f0414ff9f ['o'] + (ff9f03c9ff9fff89 +'_')[ff9f0398ff9f] + (str(ff9f03c9ff9fff89==3) +'_')[ff9fff70ff9f] + "[object Object]"[ff9fff70ff9f+ff9fff70ff9f] + (str(ff9fff70ff9f==3) +'_')[ff9f0398ff9f] + (str(ff9fff70ff9f==3) +'_')[ff9fff70ff9f - ff9f0398ff9f] + ff9f0414ff9f ['c'] + "[object Object]" [ff9fff70ff9f+ff9fff70ff9f] + ff9f0414ff9f ['o'] + (str(ff9fff70ff9f==3) +'_')[ff9f0398ff9f]
	vars_list.update({'ff9foff9f':ff9foff9f})
	#10
	ff9f0414ff9f['_'] = 'Function'
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#11
	ff9f03b5ff9f = (str(ff9fff70ff9f==3)+'_')[ff9f0398ff9f] + ff9f0414ff9f['ff9f0414ff9fff89'] + '[object Object]'[ff9fff70ff9f + ff9fff70ff9f] + (str(ff9fff70ff9f==3)+'_')[o^_^o - ff9f0398ff9f] + (str(ff9fff70ff9f==3)+'_')[ff9f0398ff9f] + (ff9f03c9ff9fff89+'_')[ff9f0398ff9f]
	vars_list.update({'ff9f03b5ff9f':ff9f03b5ff9f})
	#12
	ff9fff70ff9f = ff9fff70ff9f + ff9f0398ff9f
	vars_list.update({'ff9fff70ff9f':ff9fff70ff9f})
	#13
	ff9f0414ff9f['ff9f03b5ff9f']='\\\\';
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#14
	ff9f0414ff9f['ff9f0398ff9fff89']=('[object Object]' + str(ff9fff70ff9f))[o^_^o -(ff9f0398ff9f)]
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})
	#15
	off9fff70ff9fo=(ff9f03c9ff9fff89+'_')[c^_^o]
	vars_list.update({'off9fff70ff9fo':off9fff70ff9fo})
	#16
	ff9f0414ff9f['ff9foff9f']='\\"'
	vars_list.update({'ff9f0414ff9f':ff9f0414ff9f})

	objscode = ''

	def __init__(self, code):
		self.objscode = code

	def evalxor(self,str):
		vars = str.split('^')
		index = 0
		value = self.vars_list[vars[index].strip()]
		while index < len(vars)-1:
			value = value^self.vars_list[vars[index+1].strip()]
			index=index+1
		return value

	def aadecode(self):
		code = self.objscode.encode('unicode_escape')
		js_list = code.split(';')
		try:
			code = js_list[-3]
		except:
			return "Does not appear to be aaencoded javascript string."

		code = code.replace('\\u','')
		# This regular expression trims off the function calls. We aren't interested in executing the javascript.
		try:
			start = r'\(ff9f0414ff9f\) \[\'_\'\] \( \(ff9f0414ff9f\) \[\'_\'\] \('
			end = r'\) \(ff9f0398ff9f\)\) \(\'_\'\)'
			code = re.search(start+r'(.*?)'+end,code).group(1)
		except:
			return 'Does not appear to be aaencoded javascript string.'

		#Remove all comments from code
    	# see https://stackoverflow.com/questions/5989315/regex-for-match-replacing-javascript-comments-both-multiline-and-inline
		p = re.compile('\/\*.+?\*\/|\/\/.*(?=[\n\r])')
		code = p.sub('',code)

		results = self.decode(code)
		return results

	def decode(self,encoded_javascript):
		# At this point we have the pure encoded javascript. 
		# Split all the code by plus sign.
		code_list = encoded_javascript.split('+')
		new_list = []
		idx=0

		# This is where the decoding happens. It is the previously declared variables concatenated, summed or subtracted and encoded in ascii and escaped.
		while idx<len(code_list):
			code = code_list[idx].strip()
			#First get all the values in single parentheses and evaluate them
			if code.startswith('(') and not code.startswith('((') and code.endswith(')') and not code.endswith('))') and not '[' in code:
				code = code.replace('(','')
				code = code.replace(')','')
				if '^' not in code:
					code = self.vars_list[code]
					new_list.append(code)
				else:
					value = self.evalxor(code)
					new_list.append(value)
				idx=idx+1
			#These are the dictionaries or objects in js. They take the form (object)[attribute]
			elif '[' in code and code.endswith(']'):
				code = code.replace('(','')
				code = code.replace(')','')
				array_rep = code.split('[')
				array_rep[1] = array_rep[1].replace(']','')
				code = self.vars_list[array_rep[0]][array_rep[1]]
				new_list.append(code)
				idx=idx+1
			#At the end there is an object that has another variable after it so it doesn't end in a bracket.
			# it only occurs once and it's only a quotation mars so it is safe to delete. 
			# This may be an error an this check might be unnecessary
			elif '[' in code and not code.endswith(']'):
				new_list.append(code)
				idx=idx+1
			#The stuff in double paranthesis seems to be arithmetic. 
			elif code.startswith('(('):
				while not code.endswith('))'):
					idx=idx+1
					code = code + '+' + code_list[idx].strip()
				#I just assume there will only be two values to add or subtract
				if '+' in code:
					add_this = code.split('+')
					index=0
					while index < len(add_this):
						add_this[index] = add_this[index].replace('(','').replace(')','')
						# This evaluates the xor that occur as (o^_^o) or similar
						if '^' in add_this[index]:
							add_this[index] = self.evalxor(add_this[index])
						else:
							add_this[index] = self.vars_list[add_this[index]]
						index = index+1
					code = add_this[0] + add_this[1]

				# Essentially the same as the adding loop but subtracting.
				elif '-' in code:
					sub_this = code.split('-')
					index=0
					while index < len(sub_this):
						sub_this[index] = sub_this[index].replace('(','').replace(')','')
						if '^' in sub_this[index]:
							sub_this[index] = self.evalxor(sub_this[index])
						else:
							sub_this[index] = self.vars_list[sub_this[index].strip()]
						index=index+1
					code = sub_this[0] - sub_this[1]
			
				new_list.append(code)
				idx=idx+1
			else:
				#The default if the variable just occurs with no parenthesis or brackets. 
				code = self.vars_list[code]
				new_list.append(code)
				idx=idx+1

		#put it all together. Remove the first and second elements because they are return\" 
		#we don't need the last element either, it was never evaluated, I think it comes out to a quotation mark
		#in any case unecessary
		complete = ''
		idx = 2
		while idx < len(new_list) - 1:
			complete = complete+str(new_list[idx])
			idx=idx+1

		# Since the code is escape ascii encoded, decode twice to get unicode. 
		return complete.decode('unicode_escape').decode('unicode_escape').strip()

