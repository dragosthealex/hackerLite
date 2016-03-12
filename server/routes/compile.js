var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;
var fs = require('fs');
var twilio = require('twilio');

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
}) //router.post1

var sendMessageBack = function(output){
    // Twilio Credentials
    var accountSid = 'AC49beb2b0ce8058005d7db2504507a09f';
    var authToken = '86bafd16b3b70d18e85e051fefddb6f1';

    //require the Twilio module and create a REST client
    var twilio = require('twilio');
    var client = new twilio.RestClient(accountSid, authToken);
};

router.post('/message', function(req, res){
    //get the message Sid
    var messageSid = req.body.SmsMessageSid
    
    // Twilio Credentials
    var accountSid = 'AC49beb2b0ce8058005d7db2504507a09f';
    var authToken = '86bafd16b3b70d18e85e051fefddb6f1';

    //require the Twilio module and create a REST client
    var twilio = require('twilio');
    var client = new twilio.RestClient(accountSid, authToken);

    client.messages(messageSid).get(function(err, message) {
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

            console.log("File was written");
            //File is written at this point. Now run the python script
            exec('python interpreter.py ' + lolaFileName + ' ' + pythonFileName, function(err, stdout, sterr){
                if(err)
                    console.log(err);

                //Delete the temporary lola and python apps
                fs.unlink(lolaFileName);
                fs.unlink(pythonFileName);

                console.log("Send sms back");

                client.sms.messages.create({
                    to: '+447733645724',
                    from: '+441376350104',
                    body: stdout
                }, function(err, message) {
                    if(!err)
                        console.log(message.sid);
                    else
                        console.log(err);
                });

                //Send the resut of the compiling back
                res.json({compileResult: stdout});
            }); //exec01
        }); //writeFile1
    });
})

router.post

//return the router
module.exports = router;