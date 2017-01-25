import wiki_vocab as wv

list1 = ['stack', 'queue', 'tree', 'algorithm', 'tab']
list2 = ['object', 'semantics', 'comma', 'trombone', 'recursion']
lang1 = 'de'
lang2 = 'zh'

vocablist1 = wv.batch_find(list1, lang1)
vocablist2 = wv.batch_find(list2, lang2)

resultfile = open("result.txt","w")
resultfile.write(str(vocablist1))
print()
resultfile.write(str(vocablist2))
resultfile.close()
