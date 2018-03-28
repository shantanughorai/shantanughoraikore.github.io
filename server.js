var express = require('express');
var bodyParser = require('body-parser');
var lambdaFunc = require('./lambdaUploadApiIntegrate.js');
var app = express();
var port = process.env.PORT || 8080;
var server = require('http').Server(app);
var Promise = require('bluebird');
var multer  = require('multer');
var Storage = multer.diskStorage({
    destination: function (req, file, callback) {
        callback(null, "./tmp");
    },
    filename: function (req, file, callback) {
        callback(null, file.originalname);
    }
});
let upload  = multer({storage: Storage});

function isEmpty(obj) {
	for (var key in obj) {
		if (obj.hasOwnProperty(key))
			return false;
	}
	return true;
}

app.use(bodyParser.urlencoded({
	extended: true
}));

app.use(bodyParser.json());

app.get('/lambda', function (req, res) {
	console.log("Welcome");
	res.send("Welcome");
});

app.post('/lambda/create', upload.single('fileLoc'), (req, res) => {
    console.log(req.body);
	var body = req.body;
	var file = req.file;
	var accessKey = body.key;
	var funcName = body.funcName;
	var handlerName = body.handler;
	var apiGatewayName = body.apiName;
	lambdaFunc.createLambdaFunc(file,accessKey,funcName,handlerName,apiGatewayName).then(function(results){
			res.status(200);
			res.send('UUID to get status: '+ results);				
		}).catch(function(err){
			res.status(200);
			res.send(err);
		})
});


app.post('/lambda/status', function(req,res){
	console.log(req.body);
    var body = req.body;
	var funcId = body.funcId;
	if(!isEmpty(body)){
		lambdaFunc.readFromNeDb(funcId).then(function(results){
			res.status(200);
			res.send('Current Status: '+ results);	
		}).catch(function(err){
			res.status(200);
			res.send(err);
		})
	} else {
        console.log("Body is empty");
        res.status(200);
        res.send('Body cannot be empty');
        }
})

server.listen(port, function () {
	console.log('Our app is running on http://localhost:' + port);
});
