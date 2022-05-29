def FindDuplicate(geted_str):
	words_count = len(geted_str.split(' '))
	words = geted_str.split(' ')
	i = 0
	result = 0
	while i < words_count:
		find_first = geted_str.find(' ' + words[i] + ' ')
		find_last = geted_str.rfind(' ' + words[i] + ' ')
		if find_last != find_first:
			result = 1
		i += 1 
	if result == 1:
		return True
	else:
		return False
