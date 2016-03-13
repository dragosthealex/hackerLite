angular.module('starter.controllers', [])

.controller('DashCtrl', function($scope) {})

.controller('ChatsCtrl', function($scope, Chats) {
  // With the new view caching in Ionic, Controllers are only called
  // when they are recreated or on app start, instead of every page change.
  // To listen for when this page is active (for example, to refresh data),
  // listen for the $ionicView.enter event:
  //
  //$scope.$on('$ionicView.enter', function(e) {
  //});

  $scope.chats = Chats.all();
  $scope.remove = function(chat) {
    Chats.remove(chat);
  };
})

.controller('ChatDetailCtrl', function($scope, $stateParams, Chats) {
  $scope.chat = Chats.get($stateParams.chatId);
})

.controller('AccountCtrl', function($scope) {
  $scope.settings = {
    enableFriends: true
  };
})

.controller('TutorialCtrl', function($scope, $http) {
  $scope.lessons = [];

  $http.get('js/data.json')
  .then(function(response) {
    response.data.forEach(function(entry){
        $scope.lessons.push(entry);
    })
  });
  
})

.controller('LessonCtrl', function($scope, $http, $rootScope, $stateParams) {
  $scope.lessonId = $stateParams.lessonId;
  $scope.lessons = [];

  $http.get('js/data.json')
  .then(function(response) {
    response.data.forEach(function(entry){
      $scope.lessons.push(entry);
    });

    $scope.lessons.forEach(function(entry){
        if(entry.lesson_id == $scope.lessonId){
          $scope.task = entry.task;
        }
      });

    $scope.showChallenge = false;

    $scope.hideButton = function(){
      document.getElementById('start_btn').style.display = 'none';

      try {
        $rootScope.editor = CodeMirror.fromTextArea(document.getElementById("editor"), {
          lineNumbers: false,
          gutters: ["CodeMirror-linenumbers", "breakpoints"]
      });
          
      } catch (e) {
        console.log(e.toString())
      }
    }

    // Function call somewhere in the code:
    // -------------------------------------

    var resultMessage = [];
    var validateId;
    function validate(delay, codeToValidate) {
        if (validateId) {
            window.clearTimeout(validateId);
        }

        validateId = window.setTimeout(function () {
            var result, syntax, errors, i;
            code = codeToValidate;
            result = document.getElementById('info');

            try {
                syntax = esprima.parse(code, { tolerant: true, loc: true });
                errors = syntax.errors;
                if (errors.length > 0) {
                    result.innerHTML = 'Invalid code. Total issues: ' + errors.length;
                    console.log('Invalid code. Total issues: ' + errors.length);
                    for (i = 0; i < errors.length; i += 1) {
                        $rootScope.editor.addErrorMarker(errors[i].index, errors[i].description);
                        console.log(errors[i].index + " " + errors[i].description)
                        resultMessage = [false,errors[i].description]
                    }
                    result.setAttribute('class', 'alert-box alert');
                } else {
                    result.innerHTML = 'Yey! Your code is syntactically valid.';
                    result.setAttribute('class', 'alert-box success');
                     resultMessage = [true,'Code is syntactically valid.'];
                    if (syntax.body.length === 0) {
                        result.innerHTML = 'Empty code. Nothing to validate.';
                        console.log('Empty code. Nothing to validate.')
                    }
                }
            } catch (e) {
                //window.editor.addErrorMarker(e.index, e.description);
                console.log(e.toString())
                var n = parseInt(e.toString().match(/Line [0-9]+/)[0].match(/[0-9]+/)[0]);
                var info = $rootScope.editor.lineInfo(n);
                $rootScope.editor.setGutterMarker(n, "breakpoints", info.gutterMarkers ? null : makeMarker());
                result.innerHTML = "Oops it looks like there is something wrong: " + e.toString();
                result.setAttribute('class', 'alert-box alert');
            }

            validateId = undefined;
        }, delay || 811);
    }

    function liloToJS(){
      var code = $rootScope.editor.getValue();
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
      //lazyEvalOneLiner(code)
    }

    $scope.submitCode = function(){
      console.log("I try to submit the code");
      liloToJS();
    }

    console.log("I work!");

    $scope.$on("$ionicView.loaded", function() {
      console.log("I am getting here");
      //Put your script in here!

    });
  });



})

.controller('ChallengeCtrl', function($scope, $http, $stateParams) {
  console.log("challenge gkhgdjhr " + $stateParams.lessonId);
})

.controller('WelcomeCtrl', function($scope, $state, $q, UserService, $ionicLoading) {
  // This is the success callback from the login method
  var fbLoginSuccess = function(response) {
    if (!response.authResponse){
      fbLoginError("Cannot find the authResponse");
      return;
    }

    var authResponse = response.authResponse;

    getFacebookProfileInfo(authResponse)
    .then(function(profileInfo) {
      // For the purpose of this example I will store user data on local storage
      UserService.setUser({
        authResponse: authResponse,
        userID: profileInfo.id,
        name: profileInfo.name,
        email: profileInfo.email,
        picture : "http://graph.facebook.com/" + authResponse.userID + "/picture?type=large"
      });
      $ionicLoading.hide();
      $state.go('app.home');
    }, function(fail){
      // Fail get profile info
      console.log('profile info fail', fail);
    });
  };

  // This is the fail callback from the login method
  var fbLoginError = function(error){
    console.log('fbLoginError', error);
    $ionicLoading.hide();
  };

  // This method is to get the user profile info from the facebook api
  var getFacebookProfileInfo = function (authResponse) {
    var info = $q.defer();

    facebookConnectPlugin.api('/me?fields=email,name&access_token=' + authResponse.accessToken, null,
      function (response) {
        console.log(response);
        info.resolve(response);
      },
      function (response) {
        console.log(response);
        info.reject(response);
      }
    );
    return info.promise;
  };

  //This method is executed when the user press the "Login with facebook" button
  $scope.facebookSignIn = function() {
    facebookConnectPlugin.getLoginStatus(function(success){
      if(success.status === 'connected'){
        // The user is logged in and has authenticated your app, and response.authResponse supplies
        // the user's ID, a valid access token, a signed request, and the time the access token
        // and signed request each expire
        console.log('getLoginStatus', success.status);

        // Check if we have our user saved
        var user = UserService.getUser('facebook');

        if(!user.userID){
          getFacebookProfileInfo(success.authResponse)
          .then(function(profileInfo) {
            // For the purpose of this example I will store user data on local storage
            $scope.userID = profileInfo.id;
            $scope.name = profileInfo.name;
            UserService.setUser({
              authResponse: success.authResponse,
              userID: profileInfo.id,
              name: profileInfo.name,
              email: profileInfo.email,
              picture : "http://graph.facebook.com/" + success.authResponse.userID + "/picture?type=large"
            });

            $scope.listen = function(){
              console.log('Listen function');

              var user = {
                authResponse: success.authResponse,
                userID: profileInfo.id,
                name: profileInfo.name,
                email: profileInfo.email,
                picture : "http://graph.facebook.com/" + success.authResponse.userID + "/picture?type=large"
              }

              //send post request to get the file and its content
              $http.post('http://8e5b26b4.ngrok.io/listen', user)
                  .success(function(data, status){
                      console.log(data);
                      console.log('Listen send OK');
                  })
                  .error(function(data, status){
                      console.log("Error to the post request for the file content in angular");
                  });
            };

            $state.go('app.home');
          }, function(fail){
            // Fail get profile info
            console.log('profile info fail', fail);
          });
        }else{
          $state.go('app.home');
        }
      } else {
        // If (success.status === 'not_authorized') the user is logged in to Facebook,
        // but has not authenticated your app
        // Else the person is not logged into Facebook,
        // so we're not sure if they are logged into this app or not.

        console.log('getLoginStatus', success.status);

        $ionicLoading.show({
          template: 'Logging in...'
        });

        // Ask the permissions you need. You can learn more about
        // FB permissions here: https://developers.facebook.com/docs/facebook-login/permissions/v2.4
        facebookConnectPlugin.login(['email', 'public_profile'], fbLoginSuccess, fbLoginError);
      }
    });
  };


});