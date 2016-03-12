
var editor;
document.addEventListener("DOMContentLoaded", function(event) { 
  
  //lazyEval('myjscode');
  try {
  	editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
		    lineNumbers: true
		});
  	liloToJS();
  
        
    } catch (e) {
    	console.log(e.toString())
    }
});


function liloToJS(){
	var code = editor.getValue();
	var result = "";
	
	code = code.replace(/box/g, "var");
	code = code.replace(/=/g, "==");
	code = code.replace(/<-/g, "=");
	code = code.replace(/end/g, "}");
	code = code.replace(/call/g, "");
	code = code.replace(/dog/g, "function");
	var lines = code.split('\n');
	for(var i = 0;i < lines.length;i++){
	    //code here using lines[i] which will give you each line
	    if(lines[i].match(/if /) != null || lines[i].match(/while/) != null || lines[i].match(/function/) != null)
	    	lines[i] += "{\n";
	    else if(lines[i].match(/else/) != null)
	    	lines[i] = lines[i].replace(/else/, "}else") + "{\n";
	    else if(lines[i].match(/say/) != null)
	    	lines[i] = lines[i].replace(/say/, "console.log(") + ")\n";
	    else
	    	lines[i] += "\n";
	    result += lines[i];
	}
	code =result;
	
	

	console.log(code)
	validate(55,code);
	lazyEvalOneLiner(code)

}

// JS helper functions:
// -----------------------

var validateId;


// JS one-liner function:
// -----------------------

function lazyEvalOneLiner(code) {
	
    (0,eval)(code.replace(/^[\s\xA0]+\/\*|\*\/[\s\xA0]+$/g, ""))
}

// Function call somewhere in the code:
// -------------------------------------

var resultMessage = [];
function validate(delay, codeToValidate) {
    if (validateId) {
        window.clearTimeout(validateId);
    }

    validateId = window.setTimeout(function () {
        var result, syntax, errors, i;
        code = codeToValidate;


        try {
            syntax = esprima.parse(code, { tolerant: true, loc: true });
            errors = syntax.errors;
            if (errors.length > 0) {
                //result.innerHTML = 'Invalid code. Total issues: ' + errors.length;
                console.log('Invalid code. Total issues: ' + errors.length);
                for (i = 0; i < errors.length; i += 1) {
                    //window.editor.addErrorMarker(errors[i].index, errors[i].description);
                    console.log(errors[i].index + " " + errors[i].description)
                    resultMessage = [false,errors[i].description]
                }
                result.setAttribute('class', 'alert-box alert');
            } else {
                //result.innerHTML = 'Code is syntactically valid.';
                //result.setAttribute('class', 'alert-box success');
                 resultMessage = [true,'Code is syntactically valid.'];
                if (syntax.body.length === 0) {
                    //result.innerHTML = 'Empty code. Nothing to validate.';
                    console.log('Empty code. Nothing to validate.')
                }
            }
        } catch (e) {
            /*window.editor.addErrorMarker(e.index, e.description);
            result.innerHTML = e.toString();
            result.setAttribute('class', 'alert-box alert');
            */

             console.log(e.toString())
        }

        validateId = undefined;
    }, delay || 811);
}