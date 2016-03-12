var express = require('express');
var router = express.Router();
var exec = require('child_process').exec;
var fs = require('fs');
var path = require('path');

//Give a file number that is not used to the file
var findFileNumber = function(){
    var number;
    do{
        number = Math.random(0, 999999999); 
    }while(path.existsSync('lola' + number + '.txt'))
}   

router.post('/compile', function(req, res){
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
            res.json({compileResult: stdout});1
        }); //exec01
    }); //writeFile1
}) //router.post1

//return the router
module.exports = router;