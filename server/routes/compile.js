var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;
var fs = require('fs');
var twilio = require('twilio');
var HashMap = require('hashmap');

var hashmap = new HashMap();

// Twilio Credentials
var accountSid = 'AC49beb2b0ce8058005d7db2504507a09f';
var authToken = '86bafd16b3b70d18e85e051fefddb6f1';

var fileContent = {};

//require the Twilio module and create a REST client
var twilio = require('twilio');
var client = new twilio.RestClient(accountSid, authToken);

//Give a file number that is not used to the file
var findFileNumber = function(){
    number = Math.random(0, 999999999); 
    return number;
} 

router.post('/', function(req, res){
    //Get the sent source code of the program
    var sourceCode = req.body.sourceCode;

    //Find an unused fileNumber
    var fileNumber = findFileNumber();

    //Get a random name for the file
    var lolaFileName = 'lola' + fileNumber + '.txt';
    var pythonFileName = 'python' + fileNumber + '.py';

    //Put the sourceCode in a file
    fs.writeFile(lolaFileName, sourceCode, function(err){
        if(err)
            console.log(err);

        //File is written here. Now run the python script
        exec('python ' + lolaFileName + ' ' + pythonFileName, function(err, stdout, sterr){
            if(err)
                console.log(err);

            //Delete the temporary lola and python apps
            fs.unlink(lolaFileName);
            fs.unlink(pythonFileName);

            //Send the resut of the compiling back
            res.json({compileResult: stdout});
        }); //exec01
    }); //writeFile1
}); //router.post1

var chunkSize = 20;
var senderPhoneNumber;

var sendInChunks = function(output, leftEnd, rightEnd){
    var messageSize = output.length;
    
    var text = output.substring(leftEnd, rightEnd);

    client.sms.messages.create({
        to: senderPhoneNumber,
        from: '+441376350104',
        body: text
    }, function(err, message) {
        if(!err)
            console.log(message.sid);
        else
            console.log(err);
        leftEnd += chunkSize;
        rightEnd = Math.min(rightEnd + chunkSize, messageSize);

        if(leftEnd < messageSize)
            sendInChunks(output, leftEnd, rightEnd);
    });
};

var attach = function(code, phone, filename){
    
    var finish = 0;
    if(code.indexOf('#ec') > -1){
        finish = 1;
        code = code.replace('#ec', '');
    }

    data = hashmap.get(phone);
    if(data == undefined)
        data = '';

    console.log('HashMap');
    console.log(data);
    data = data + '\n' + code;
    hashmap.set(phone, data);

    if(finish == 1){
        console.log(filename);
        fs.writeFile(filename, data, function(err){
            if(err)
                console.log(err);
            var pythonFileName = filename.replace('lola', 'python');
            pythonFileName = pythonFileName.replace('.txt', '.py');

            //File is written at this point. Now run the python script
            exec('python interpreter.py ' + filename + ' ' + pythonFileName, function(err, stdout, sterr){
                if(err)
                    console.log(err);

                //Delete the temporary lola and python apps
                //fs.unlink(lolaFileName);
                //fs.unlink(pythonFileName);

                console.log("Send sms back");

                stdout = data;

                console.log("Code is");
                console.log(stdout);
                var rightEnd = Math.min(chunkSize, stdout.length);
                sendInChunks(stdout, 0, rightEnd);

                //Send the resut of the compiling back
                //res.json({compileResult: stdout});
            }); //exec01
        });
    }
}

router.post('/message', function(req, res){

    //get the message Sid
    var messageSid = req.body.SmsMessageSid

    client.messages(messageSid).get(function(err, message) {
        //Get the sent source code of the program
        var sourceCode = message.body;

        //get the phone number of the sender
        senderPhoneNumber = message.from;
        senderPhoneNumber = senderPhoneNumber.replace('+', '');
        console.log(senderPhoneNumber);

        //Find an unused fileNumber
        //var fileNumber = findFileNumber();

        //Get a random name for the file
        var lolaFileName = 'lola' + senderPhoneNumber + '.txt';
        var pythonFileName = 'python' + senderPhoneNumber + '.py';

        if(sourceCode.indexOf('#bc') > -1){
            sourceCode = sourceCode.replace('#bc', '');
            console.log(sourceCode);
            hashmap.set(senderPhoneNumber, '');
            attach(sourceCode, senderPhoneNumber, lolaFileName);
        }
        else{
            attach(sourceCode, senderPhoneNumber, lolaFileName);
        }
    });
});

//return the router
module.exports = router;