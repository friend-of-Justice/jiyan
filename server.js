var express = require("express")
var sdk1 = require("./w1.js")
var sdk2 = require("./w2.js")
var bodyParser = require('body-parser')
var api = express()
api.use(bodyParser.urlencoded({
    parameterLimit:50000,
    limit:"50mb",
    extended:false
}));

api.post('/get_w1',function(req,res){
    var gt = req.body.gt
    var challenge = req.body.challenge
    var token = sdk1.get_w1(gt,challenge)
    res.send(token)
}); 

api.post('/get_w2',function(req,res){
    var gt = req.body.gt
    var challenge = req.body.challenge
    var s = req.body.s
    var c = req.body.c
    var token_ymml = req.body.token_ymml
    var token = sdk2.get_w2(gt,challenge,c,s,token_ymml)
    res.send(token)
}); 


var server = api.listen(8898,function(){

})
