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

.controller('LessonCtrl', function($scope, $http, $stateParams) {
  console.log("state params is " + $stateParams.lessonId);
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