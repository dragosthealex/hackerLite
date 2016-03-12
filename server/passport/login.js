'use strict';

var LocalStrategy = require('passport-local').Strategy;
var User = require('./user');
var bCrypt = require('bcrypt-nodejs');

module.exports = function(passport) {

  passport.use('local-login', new LocalStrategy({
      passReqToCallback: true 
    },
    function(req, username, password, done) {
        //Check if the user is in the databse
        User.findOne({ 'username' : username },
          function(err, user) {
            //In case of error, return error
            if (err)
              return done(err);
            //Username does not exist in the database
            if(!user) {
              console.log('No user found with username: ' + username);
              return done(null, false, 
                          req.flash('message', 'User not found.'));
            }
            //User exists but wrong password
            if(!isValidPassword(user, password)) {
              console.log('Invalid Password');
              return done(null, false,
                          req.flash('message', 'Invalid password'));
            }
            //Everthing is OK
            return done(null, user);
          }
        );
    }));

  var isValidPassword = function(user, password) {
    return bCrypt.compareSync(password, user.password);
  }
};