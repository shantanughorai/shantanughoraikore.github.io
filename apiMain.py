from apiTests import testApi
import csv
import json
myData = []

testApi = testApi()

with open("testCases.csv") as csvFile:
	readCsv = csv.reader(csvFile,delimiter = ',')
	for row in readCsv:
		print("Test case being executed: "+ str(row))
		rowData=[]
		if row[0].lower() == "test":
			rowData.append(row[0])
			rowData.append(row[1])
			rowData.append("Status")
			myData.append(rowData)
		elif row[0].lower()=="list":
			rowData.append(row[0])
			rowData.append(row[1])
			#print(row[1])
			result = testApi.listEntity(row[1])
			if json.loads(result):
				rowData.append("PASSED")
				myData.append(rowData)
			else:
				rowData.append("FAILED")
				myData.append(rowData)
		elif row[0].lower()=="create":
			rowData.append(row[0])
			rowData.append(row[1])
			result = testApi.createEntity(row[1])
			#print(result)
			if result == "Invalid resource":
				rowData.append(result)
				myData.append(rowData)
			elif json.loads(result):
				#print(result)
				rowData.append("PASSED")
				myData.append(rowData)
			else:
				rowData.append("FAILED")
				myData.append(rowData)
		elif row[0].lower()=="show":
			rowData.append(row[0])
			rowData.append(row[1])
			testData = row[1].split(" ")
			if len(testData)>1:
				result = testApi.showEntity(testData[0],testData[1])
				if json.loads(result):
					rowData.append("PASSED")
					myData.append(rowData)
				else:
					rowData.append("FAILED")
					myData.append(rowData)
			else:
				result = testApi.showEntity(testData[0],1)
				if json.loads(result):
					rowData.append("PASSED")
					myData.append(rowData)
				else:
					rowData.append("FAILED")
					myData.append(rowData)
		elif row[0].lower()=="delete":
			rowData.append(row[0])
			rowData.append(row[1])
			testData = row[1].split(" ")
			if len(testData)>1:
				result = testApi.deleteEntity(testData[0],testData[1])
				if json.loads(result):
					rowData.append("FAILED")
					myData.append(rowData)
				else:
					rowData.append("PASSED")
					myData.append(rowData)
			else:
				result=testApi.deleteEntity(testData[0],1)
				if json.loads(result):
					rowData.append("FAILED")
					myData.append(rowData)
				else:
					rowData.append("PASSED")
					myData.append(rowData)
		elif row[0].lower()=="filter":
			rowData.append(row[0])
			rowData.append(row[1])
			testData=rowData[1].split(" ")
			if len(testData)==3:
				result=testApi.filterEntity(testData[0],testData[1],testData[2])
				if json.loads(result):
					#print(json.dumps(result))
					result = json.loads(result)
					#print(result[0]["userId"])
					if str(result[0]["userId"]) == str(testData[2]):
						rowData.append("PASSED")
						myData.append(rowData)
					else:
						rowData.append("FAILED")
						myData.append(rowData)
				else:
					rowData.append("FAILED")
					myData.append(rowData)
			else:
				rowData.append("Test case not proper")
				myData.append(rowData)
		elif row[0].lower()=="update":
			rowData.append(row[0])
			rowData.append(row[1])
			testData=row[1].split(" ")
			if len(testData)==3:
				result=testApi.updateEntity(testData[0],testData[1],testData[2])
				if json.loads(result):
					#print(json.dumps(result))
					result = json.loads(result)
					if result[2]==testData[2]:
						rowData.append("PASSED")
						myData.append(rowData)
					else:
						rowData.append("FAILED")
						myData.append(rowData)
				else:
					rowData.append("FAILED")
					myData.append(rowData)
			else:
				rowData.append("Test case not proper")
				myData.append(rowData)
#print(myData)
with open("Results.csv",'w',newline='') as writeFile:
	write = csv.writer(writeFile)
	for data in myData:
		write.writerow(data)
print("Testing completed!")
			