import requests
import json

baseUrl = "https://jsonplaceholder.typicode.com/"
header = {"Content-type": "application/json; charset=UTF-8"}	

class testApi(object):
	def __init__(self):
		pass

	def postCall(self,postData, url):
		'''Function for Post Call'''
		payload = json.dumps(postData,indent=4)
		try:
			resp = requests.post(url,data = payload, headers = header)
			result = json.loads(resp.text)
			return json.dumps(result)
		except Exception as e:
			return e

	def validateEntityCreated(self,id,entity):
		'''Function to retreive an entity'''
		url = baseUrl+entity+"/"+str(id)
		resp = requests.get(url)
		result= json.loads(resp.text)
		return json.dumps(result)

	def createEntity(self,entity):
		'''Function to test create a resource. Following resources are created and validates if created or not.
		Resources: Posts, Albums, Photos, Users, Comments and ToDos.
		If a resouce is not present it returns exception "Invalid entity"
		'''	
		if entity.lower() == "posts":
			data = {
			"title": "foo",
			"body": "bar",
			"userId": 1
			}
			payload = json.dumps(data, indent=4)
			url = baseUrl+entity
			result = self.postCall(data,url)
			result=json.loads(result)
			if result["id"]:
				newResult = self.validateEntityCreated(result["id"],entity)
				return newResult
			else:
				return result
		elif entity.lower() == "albums":
			data = {
			"userId":1,
			"title":"test title"
			}
			url = baseUrl+entity
			result = self.postCall(data,url)
			result = json.loads(result)
			if result["id"]:
				newResult = self.validateEntityCreated(result["id"],entity)
				return newResult
			else:
				return result
		elif entity.lower()=="photos":
			data = {
			"albumId":1,
			"title":"test",
			"url":"http://placehold.it/600/92c952",
			"thumbnailUrl": "http://placehold.it/150/92c952"
			}
			url = baseUrl+entity
			result=self.postCall(data,url)
			result=json.loads(result)
			if result["id"]:
				newResult=self.validateEntityCreated(result["id"],entity)
				return newResult
			else:
				return result
		elif entity.lower()=="users":
			data={
			"name": "Glenna Reichert",
			"username": "Delphine",
			"email": "Chaim_McDermott@dana.io",
			"address": {
				"street": "Dayna Park",
				"suite": "Suite 449",
				"city": "Bartholomebury",
				"zipcode": "76495-3109",
				"geo": {
					"lat": "24.6463",
					"lng": "-168.8889"
				}
			},
			"phone": "(775)976-6794 x41206",
			"website": "conrad.com",
			"company": {
				"name": "Yost and Sons",
				"catchPhrase": "Switchable contextually-based project",
				"bs": "aggregate real-time technologies"
				}
			}
			url = baseUrl+entity
			result=self.postCall(data,url)
			result=json.loads(result)
			if result["id"]:
				newResult=self.validateEntityCreated(result["id"],entity)
				return newResult
			else:
				return result
		elif entity.lower()=="comments":
			data = {
				"postId": 1,
				"name": "id labore ex et quam laborum",
				"email": "Eliseo@gardner.biz",
				"body": "test comments"
			}
			url = baseUrl+entity
			result=self.postCall(data,url)
			result=json.loads(result)
			if result["id"]:
				newResult=self.validateEntityCreated(result["id"],entity)
				return newResult
			else:
				return result
		elif entity.lower()=="todos":
			data = {
				"userId":1,
				"title": "test todo",
				"completed":"false"
			}
			url = baseUrl+entity
			result=self.postCall(data,url)
			result=json.loads(result)
			if result["id"]:
				newResult=self.validateEntityCreated(result["id"],entity)
				return newResult
			else:
				return result
		else:
			return "Invalid resource"

	def showEntity(self,entity,id):
		'''Function to test Show resources. Tests inputs with invalid resource ids'''
		result = self.validateEntityCreated(id,entity)
		return result

	def listEntity(self,entity):
		'''Function to test listing of resources. Validates invalid resource name as well'''
		url = baseUrl+entity
		resp = requests.get(url)
		result = json.loads(resp.text)
		return json.dumps(result)

	def deleteEntity(self,entity,id):
		'''Function to delete an entity and check if tis deleted or not'''
		url = baseUrl+entity+"/"+id
		result=requests.delete(url,headers=header)
		result = json.loads(result.text)
		newResult=self.validateEntityCreated(id,entity)
		return json.dumps(newResult)

	def updateEntity(self,entity,id, updateText):
		'''Function to update an entity and return the updated entity'''
		payload = {
			"id":id,
			"title":updateText,
			"body":"foo",
			"userId":1
		}
		url = baseUrl+entity+"/"+str(id)
		result = requests.put(url,data=payload,headers=header)
		newResult=self.validateEntityCreated(id,entity)
		return json.dumps(newResult)

	def filterEntity(self,entity,filterField,id):
		url = baseUrl+entity+"?"+filterField+"="+str(id)
		result = requests.get(url,headers=header)
		result = json.loads(result.text)
		return json.dumps(result)

	def __del__(self):
		pass