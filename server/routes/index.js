var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Express' });
});

var passportRouter = function(passport) {
    //signup
    router.post('/signup', passport.authenticate('local-signup', {
      successRedirect: '/', //Use the app
      failureRedirect: '/signup', //Try to sign up again
      failureFlash: true
    }));
}

module.exports = passportRouter;
