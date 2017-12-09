import xmltodict



file = open("log.xml", "r")
xml = file.read()


print (xmltodict.parse(xml))
