var AWS = require('aws-sdk');
var parentId,restApiId, newParentId, funcUri;
AWS.config.region = 'us-east-2';
var region = 'us-east-2';
var apig = new AWS.APIGateway({apiVersion: '2015/07/09'/* '2015/07/09' */});
var lambda = new AWS.Lambda();
var fs = require('fs');
var deployedUrl;
var Promise = require('bluebird');
var uuid = require('node-uuid');
var Datastore = require('nedb');
var lambdaStatus = new Datastore({filename: 'status.db', autoload: true});

function readFromNeDb(funcUid){
	return new Promise(function(resolve,reject){
		lambdaStatus.find({'funcId': funcUid}).sort({ timeStamp: -1 }).limit(1).exec(function (err, docs) {
			if(!err) {
				if(docs.length > 0) {
				console.log(JSON.stringify(docs[0].newStatus));
				resolve(JSON.stringify(docs[0].newStatus));
				} 
			} else {
				reject(err);
			}		
	});
	})
}

function uploadToS3(file){
	var s3 = new AWS.S3();
	console.log(file);
	var fileName = file.originalname;
	var fileRead = file.path;
	return new Promise(function(resolve,reject){
		console.log("logging file");
		var s3params = {
					Bucket : 'aws-lambda-kore-botkit',
					Key : fileName,
					Body : fs.createReadStream(fileRead)
				};
		console.log(JSON.stringify(s3params));
		s3.putObject( s3params, function( err, data ){
			if (err) {
				reject(err);
			} else {
				resolve(data);
			}
		})		
	})
	
}

function createLambda(file,funcName,handler){
	var lambda = new AWS.Lambda();
	var params = {
		Code: { 
			S3Bucket: 'aws-lambda-kore-botkit',
			S3Key : file.filename
		},
		FunctionName: funcName,
		Handler: handler,
		Role: "arn:aws:iam::452460288037:role/lambda_basic_execution", 
		Runtime: "nodejs6.10" 
		};	
	return new Promise(function(resolve,reject){
		console.log("Inside create lambda");
		console.log(params);
		lambda.createFunction(params, function(err, data) {
               	if (err){
					 reject(err, err.stack);
				} // an error occurred
          		else {
					console.log(data);
					funcUri = data.FunctionArn;
					console.log('Lambda URI: '+funcUri);
					resolve(null);
				}                
			});
	})
}

function createApi(apiName){
	console.log("Inside create API");
	return new Promise (function(resolve, reject){
		apig.createRestApi({
			name: apiName,
			binaryMediaTypes: ['*'],
			description: "Demo API created using the AWS SDK for node.js",
			version: "0.00.001"
	}, function(err, data){
		if (!err) {
			console.log("Inside function createRestApi");
			//console.log(data);
			restApiId = data.id;
			console.log(restApiId);
			//getResources(data.id, funcUri)
			resolve(null);
		} else {
			reject('Create API failed:\n', err);
			}
		})
	})
}

function getResources(){
	console.log("Inside function getResources");
	console.log("Passed Id : ",restApiId);
	//var lambdaUri = funcUri;
   return new Promise(function(resolve, reject){
	    apig.getResources({
			restApiId: restApiId
		}, function(err, data){
			if (!err) {
				console.log(data);
				parentId = data.items[0].id;
				console.log("Parent Id",parentId);
				//createResource(_restApiId,parentId, lambdaUri)
				resolve(null);
			} else {
            //console.log('Get the root resource failed:\n', err);
			reject('Get the root resource failed:\n', err);
			}
		})
   })
}

function createResource(){
	//var lambdaUri = lambdaUri
	console.log("Inside function createResource");
	console.log("Rest API ID: "+restApiId);
	console.log("Parent Id",parentId);
	return new Promise(function(resolve, reject){
		  apig.createResource({
			restApiId: restApiId,
			parentId: parentId,
			pathPart: '{proxy+}'//'pets'
		}, function(err, data){
			if (!err) {
				console.log(data);
				console.log("New ParentId :",data.id);
				newParentId = data.id;
				//apiPutMethod(data.id, lambdaUri);
				resolve(null);
			} else {
            //console.log("The '/pets' resource setup failed:\n", err);
			reject("The '/pets' resource setup failed:\n", err);
			}	
		})
	})
}

function apiPutMethod(){
	console.log("Inside function apiPutMethod");
	console.log("New parent id is: ", newParentId);
	return new Promise(function(resolve, reject){
		apig.putMethod({
			restApiId: restApiId,
			resourceId: newParentId,
			httpMethod: 'ANY',
			authorizationType: 'NONE'
		}, function(err, data){
			if (!err) {
				console.log(data);
				resolve(null);
			} else {
				reject("The 'GET /pets' method setup failed:\n", err);
			}	
		})
	})
}

function putIntegration(){
	console.log("Inside function putIntegration");
	return new Promise (function(resolve,reject){
		apig.putIntegration({
			restApiId: restApiId,
			resourceId: newParentId,
			httpMethod: 'ANY',
			type: 'AWS_PROXY',//'HTTP',
			integrationHttpMethod: 'POST',//'GET',
			uri:'arn:aws:apigateway:'+region+':lambda:path/2015-03-31/functions/'+funcUri+'/invocations'
		}, function(err, data){
			if (!err) {
				console.log(data);
				//putIntegrationRes(id,funcUri);
				resolve(null);
			} else {
            //console.log("Set up the integration of the 'GET /' method of the API failed:\n", err);
			reject ("Set up the integration of the 'GET /' method of the API failed:\n", err);
			}
        })
	})
}

function putIntegrationRes(){
	console.log("Inside function putIntegrationRes");
    return new Promise(function(resolve,reject){
		apig.putIntegrationResponse({
			restApiId: restApiId,
			resourceId: newParentId,
			httpMethod: 'ANY',
			statusCode: '200',
			selectionPattern: ''
		}, function(err, data){
			if (!err) {
				console.log(data);
				//addPermission(id,funcUri);
				resolve(null);
			} else {
				//console.log("The 'GET /pets' method integration response setup failed:\n", err);
				reject("The 'GET /pets' method integration response setup failed:\n", err);
			}				
        })
	})
}

function addPermission(){
	console.log("Inside function addPermission");
	console.log("API URL: "+restApiId);
	var funcName = funcUri;
	funcName = funcName.split(":");
    var params = {
        Action: "lambda:InvokeFunction", 
        FunctionName: funcName[6], 
        Principal: "apigateway.amazonaws.com", 
		SourceArn: 'arn:aws:execute-api:'+region+':452460288037:'+restApiId+'/*/*/*',
		StatementId: Math.floor(Math.random()*10).toString()
       };
    return new Promise(function(resolve,reject){
		lambda.addPermission(params, function (err, data) {
			if (err) {
				//console.log(err, err.stack);
				reject(err);				
			} // an error occurred
			else {
				console.log("SUCCESS :: ",data);           // successful response
				//testInvokeMethod(id);
				resolve(null);
			}  
		});
	})
}

function testInvokeMethod(){
	console.log("Inside function testInvokeMethod");
    return new Promise(function(resolve,reject){
		apig.testInvokeMethod({
			restApiId: restApiId,
			resourceId: newParentId,
			httpMethod: "ANY",
			pathWithQueryString: '/'
		}, function(err, data){
			if (!err) {
				console.log("####################### Not a error but ######################");
				console.log(data);
				resolve(null);
				//return "Test completed";
			} else {
				//console.log('Test-invoke-method on GET /pets failed:\n', err);
				reject('Test-invoke-method on GET /pets failed:\n', err);
			}
		})
	})
}

function createDeployment(){
	console.log("Inside function createDeployment");
	console.log(restApiId);
    return new Promise(function(resolve,reject){
		apig.createDeployment({
			restApiId: restApiId,
			stageName: 'prod',
			stageDescription: 'test deployment',
			description: 'API deployment'
		}, function(err, data){
			if (err) {
				//console.log('Deploying API failed:\n', err);
				reject('Deploying API failed:\n', err);
			}	else {
				console.log("Deploying API succeeded\n", data);
				//show_results(restApiId);
				resolve(null);
				//console.log("Deployed url is: https://"+restApiId+".execute-api."+region+".amazonaws.com/prod/");
			}
		})
	})
}

function show_results() {
	return new Promise(function(resolve,reject){
		if(restApiId){
			deployedUrl = 'https://'+restApiId+'.execute-api.'+region+'.amazonaws.com/prod/';
			resolve(deployedUrl);
		} else {
			reject("Rest api not yet set");
		}		
	})
}

function finalUploadFunc(file, accessKey, funcName, handler, apiName, uuidRes){
	var status = {
		funcId: uuidRes,
		funcName: funcName,
		curStatus: 'Just reached S3',
		timeStamp: new Date(),
		newStatus: ''
	};
	uploadToS3(file).then(function(){
		status.newStatus = 'Uploading '+file+' into S3Bucket  in progress...';
		status.timeStamp = new Date();
		lambdaStatus.insert(status, function(err,doc){
			console.log('Inserted', doc.name, 'with ID', doc._id);
		});
		createLambda(file,funcName,handler).then(function(){
			status.newStatus = file +' uploaded in S3 successfully. \nCreation '+funcName+' function in Lambda in progress....';
			status.timeStamp = new Date();
			lambdaStatus.insert(status, function(err,doc){
				console.log('Inserted', doc.name, 'with ID', doc._id);
			});
			createApi(apiName).then(function(){
				status.newStatus = 'Lambda Function '+funcName+' created.\nCreation of '+apiName+' api in API Gateway in progress....';
				status.timeStamp = new Date();
				lambdaStatus.insert(status, function(err,doc){
					console.log('Inserted', doc.name, 'with ID', doc._id);
				});
				getResources().then(function(){
					createResource().then(function(np){
						status.newStatus = 'API '+apiName+' created.\nCreation of API Resources in API Gateway in progress....';
						status.timeStamp = new Date();
						lambdaStatus.insert(status, function(err,doc){
							console.log('Inserted', doc.name, 'with ID', doc._id);
						});
						apiPutMethod().then(function(){	
							status.newStatus = 'API resources for '+apiName+' created.\nCreation of API methods in API Gateway in progress....';
							status.timeStamp = new Date();
							lambdaStatus.insert(status, function(err,doc){
								console.log('Inserted', doc.name, 'with ID', doc._id);
							});
							putIntegration().then(function(){
								status.newStatus = 'API methods for '+apiName+' created.\nIntegration of API '+apiName+' in progress....';
								status.timeStamp = new Date();
								lambdaStatus.insert(status, function(err,doc){
									console.log('Inserted', doc.name, 'with ID', doc._id);
								});
								putIntegrationRes().then(function(){
									addPermission().then(function(){
										status.newStatus = 'API integration for '+apiName+' completed.\nPermissions of API '+apiName+' in progress....';
										status.timeStamp = new Date();
										lambdaStatus.insert(status, function(err,doc){
											console.log('Inserted', doc.name, 'with ID', doc._id);
										});
										testInvokeMethod().then(function(){
											createDeployment().then(function(){
												show_results().then(function(results){
													status.newStatus = 'API deployed successfully. URL is:'+results;
													status.timeStamp = new Date();
													lambdaStatus.insert(status, function(err,doc){
														console.log('Inserted', doc.name, 'with ID', doc._id);
													});
													console.log("Deployed url is ", deployedUrl);
												})
											})
										})
									})
								})
							})
						})
					})
				})
			})
		})				
	});
}

function generateUuid(){
	var uuid1 = uuid.v4();
	return new Promise(function(resolve, reject){
		if(uuid1) {
			console.log("UUID from resolve: ",uuid1);
			resolve(uuid1);
		} else {
			console.log("UUID from reject: ",uuid1);
			reject("UUID not generated");
		}
	})
}

function createLambdaFunc(file, accessKey, funcName, handler, apiName){
	AWS.config.credentials.accessKeyId = accessKey;
	return generateUuid().then(function(uuidRes) {
		console.log("UUID returned is: ", uuidRes);
		finalUploadFunc(file, accessKey, funcName, handler, apiName,uuidRes);
		return uuidRes;
	});
}
module.exports.createLambdaFunc = createLambdaFunc;
module.exports.readFromNeDb = readFromNeDb;