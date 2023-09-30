var fs = require('fs');
var cli = require('cli');
var bb = require("@amida-tech/blue-button")

var filePath = cli.args[0];

var data = fs.readFileSync(filePath).toString();
var doc = bb.xml.parse(data);
var result = bb.parseXml(doc);
console.log(JSON.stringify(result));
