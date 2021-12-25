ans = []

def choose_literal(clauses):
	sm = {}
	diff = {}
	for i in list(clauses.keys()):
		for j in clauses[i]:
			if(j==1):
				sm[i] = sm.get(i,0) + 1
				diff[i] = diff.get(i,0) - 1
			if(j==0):
				sm[i] = sm.get(i,0) + 1
				diff[i] = diff.get(i,0) + 1
	mx_term = ''
	mx_val = 0
	t_or_f = {}
	for i in list(diff.keys()):
		if(diff[i] < 0):
			t_or_f[i] = False
		else:
			t_or_f[i] = True
		diff[i] = abs(diff[i])
		if(sm[i] + diff[i] > mx_val):
			mx_val = sm[i] + diff[i]
			mx_term = i
	return [mx_term, t_or_f[mx_term]]

def dpll(clauses):
	print('List of Clauses Remaining:\n')
	for i in list(clauses.keys()):
		print(i, end=' : ')
		for j in clauses[i]:
			print(j, end=' ')
		print()
	print()
	if(len(list(clauses.keys())) == 0):
		return False
	sm = 0
	for i in list(clauses.keys()):
		if(len(clauses[i])>0):
			if((clauses[i].count(0) == len(clauses[i])) or (clauses[i].count(1) == len(clauses[i]))):
				ans.append(i)
				if clauses[i][0] == 0:
					ans[-1] += '!'
				return True
	for i in list(clauses.keys()):
		if(len(clauses[i])>0):
			for j in clauses[i]:
				if (j==0) or (j==1):
					sm+=1
	if(sm==0):
		return True
	[lit, torf] = choose_literal(clauses)
	print('Choosing best literal:	'+lit)
	print('Initializing this literal:	'+lit+' = '+str(torf)+'\n')
	clause_lit = {}
	clause_opp = {}
	torf = int(torf)
	for i in range(len(clauses[lit])):
		if not(clauses[lit][i] == 1-torf):
			for j in list(clauses.keys()):
				if j==lit:
					continue
				clause_lit[j] = clause_lit.get(j,[]) + [clauses[j][i]]
		if not(clauses[lit][i] == torf):
			for j in list(clauses.keys()):
				if j==lit:
					continue
				clause_opp[j] = clause_opp.get(j,[]) + [clauses[j][i]]
	if dpll(clause_lit):
		ans.append(lit)
		if torf==1:
			ans[-1] += '!'
		return True
	else:
		print('Fail. Trying out other value:		'+lit+' = '+str(1-torf))
		if dpll(clause_opp):
			ans.append(lit)
			if torf==0:
				ans[-1] += '!'
			return True
	return False

def main():
	with open('input_file.txt','r') as f:
		variables = f.readline().split()
		clauses = {}
		for i in variables:
			clauses[i] = []
		s = f.readline()
		s = s[1:]
		s = s[:-1]
		arr = s.split(')(')
		for i in variables:
			for _ in arr:
				clauses[i].append('x')
		for i in range(len(arr)):
			temp = arr[i].split('+')
			for j in temp:
				if(len(j)==1):
					clauses[j[0]][i] = 0
				else:
					clauses[j[0]][i] = 1
	b = dpll(clauses)
	if not b:
		print('\nFail!')
		print('Clause unachievable')
	else:
		ans.reverse()
		print('\nSUCCESS!!')
		print('Clauses satisfied with following values')
		for i in ans:
			print(i[0] + ' = ', end='')
			if len(i)==1:
				print('0')
			else:
				print('1')
		return

main()