from MagicCNKI import MagicCNKI
import pprint

mc = MagicCNKI()

for i in mc.search(query='机器学习'):
	try:
		pprint.pprint(i)
	except:
		pass
		
for url in mc.search_url(query='机器学习', start=2):
	pprint.pprint(url)