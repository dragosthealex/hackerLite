'use strict';

var LocalStrategy = require('passport-local').Strategy;
var User = require('./user');
var bCrypt = require('bcrypt-nodejs');

module.exports = function(passport) {

  passport.use('local-signup', new LocalStrategy({
    passReqToCallback: true
  },
  function(req, username, password, done) {

    var findOrCreateUser = function(){
      //Find if the user is not already in the database
      User.findOne({'username' : username},
        function (err, user) {
          //In case of error return it with done
          if(err) {
            console.log('Error in signup: ' + err);
            return done(err);
          }
          else if(user) {
            //User already exists
            console.log('User already exists');
            return done(null, false,
              req.flash('message', 'User ' + username 
                        + 'is already in the databse'));
          }
          else {
            //Everything is ok
            var newUser = new User();
            
            newUser.username = username;
            newUser.password = createHash(password);
            newUser.email = req.param('email');
            newUser.firstName = req.param('firstname');
            newUser.lastName = req.param('lastname');

            //save the user
            newUser.save( function(err) {
              if(err) {
                console.log('Error in saving user: ' + err);
                throw err;
              }
              console.log('User registration succesful');
              return done(null, newUser);
            });
          }           
        });
      };

      //Delay the run of findOrCreateUser
      process.nextTick(findOrCreateUser);
    })
  );

  var createHash = function(password) {
    return bCrypt.hashSync(password, bCrypt.genSaltSync(10), null);
  }
};  