'use strict';
//Require dependencies
var yeoman = require('yeoman-generator');
var chalk = require('chalk');
var yosay = require('yosay');
var mkdirp = require('mkdirp');

function capitalizeFirstLetter(str){
   var splitStr = str.toLowerCase().split(' ');
   for (var i = 0; i < splitStr.length; i++) {
       // You do not need to check if i is larger than splitStr length, as your for does that for you
       // Assign it back to the array
       splitStr[i] = splitStr[i].charAt(0).toUpperCase() + splitStr[i].substring(1);     
   }
   // Directly return the joined string
   console.log("String Test", splitStr.join(''));
   return splitStr.join(''); 
}




module.exports = yeoman.generators.Base.extend({
//Configurations will be loaded here.
//Ask for user input
prompting: function() {
    var done = this.async();
    this.prompt(
      [
        {
          type: 'input',
          name: 'pagename',
          message: 'What is the page name?',
          //Defaults to the project's folder name if the input is skipped
          default: this.pagename
        },
        {
          type: 'input',
          name: 'slug',
          message: 'What is root slug for this page?',
          //Defaults to the project's folder name if the input is skipped
          default: this.slug
        }
      ], function(answers) {

        answers.pagenamecamel = capitalizeFirstLetter(answers.pagename);
        answers.pagenamelower = capitalizeFirstLetter(answers.pagename).toLowerCase();
        answers.slug          = capitalizeFirstLetter(answers.slug).toLowerCase();
        answers.directoryname = answers.pagenamelower + '_page';
        this.props = answers;
        this.log(answers.pagenamelower);
        this.log(answers.slug)
        done();
      }.bind(this));
  },
  writing: {
  //Copy the configuration files

  //Copy application files
  app: function(){
      //Model file
      var directoryname = this.props.directoryname;
      mkdirp(directoryname);
      mkdirp(directoryname+'/templates');
      mkdirp(directoryname+'/templates/'+directoryname);
      mkdirp(directoryname+'/migrations');
      this.copy('_migrations/__init__.py', directoryname+'/migrations/__init__.py');
      this.copy('__init__.py', directoryname + '/__init__.py');
      this.fs.copyTpl(
        this.templatePath('_models.py'),
        this.destinationPath(directoryname+'/models.py'), {
          pagenamecamel: this.props.pagenamecamel,
          pagenamelower: this.props.pagenamelower
        }
      );
      this.fs.copyTpl(
        this.templatePath('_urls.py'),
        this.destinationPath(directoryname+'/urls.py'), {
          slug: this.props.slug,
          pagenamelower: this.props.pagenamelower

        }
      );
    },
    //Install Dependencies
  },
});

//Writing Logic here


// 'use strict';
// var yeoman = require('yeoman-generator');
// var chalk = require('chalk');
// var yosay = require('yosay');

// module.exports = yeoman.generators.Base.extend({
//   prompting: function () {
//     var done = this.async();

//     // Have Yeoman greet the user.
//     this.log(yosay(
//       'Welcome to the astonishing ' + chalk.red('') + ' generator!'
//     ));

//     var prompts = [{
//       type: 'confirm',
//       name: 'someOption',
//       message: 'Would you like to enable this option?',
//       default: true
//     }];

//     this.prompt(prompts, function (props) {
//       this.props = props;
//       // To access props later use this.props.someOption;

//       done();
//     }.bind(this));
//   },

//   writing: function () {
//     this.fs.copy(
//       this.templatePath('dummyfile.txt'),
//       this.destinationPath('dummyfile.txt')
//     );
//   },

//   install: function () {
//     this.installDependencies();
//   }
// });
