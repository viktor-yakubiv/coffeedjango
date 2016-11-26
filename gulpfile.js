/**
 * IOIT Gulpfile
 * Copyright © 2016 Viktor Yakubiv
 */


/*
 * Modules
 */

var gulp = require('gulp');
var del = require('del');
var runSequence = require('run-sequence');

// Common
var filter = require('gulp-filter');
var plumber = require('gulp-plumber');
var rename = require('gulp-rename');
var sourcemaps = require('gulp-sourcemaps');

// CSS
var sass = require('gulp-sass');
var postcss = require('gulp-postcss');
var autoprefixer = require('autoprefixer');
var sorting = require('postcss-sorting');
var nano = require('cssnano');

// Images
var imagemin = require('gulp-imagemin');
var pngquant = require('imagemin-pngquant');
var resize = require('gulp-image-resize');


/*
 * Tasks
 */

gulp.task('clean', function () {
  return del(['static/css']);
});

gulp.task('js:copy', function () {
  return gulp.src([
    'bower_components/jquery/dist/jquery?(.min).js',
    'src/js/vendor/**'
  ]).pipe(gulp.dest('dist/js/vendor'));
});

gulp.task('js:plugins', function () {
  return gulp.src([
    'src/js/plugins.js',
    'bower_components/typed.js/dist/typed.min.js'
  ])
    .pipe(plumber())
    .pipe(concat('plugins.js'))
    .pipe(gulp.dest('dist/js'));
});


gulp.task('css', function (cb) {
  gulp.src('static/scss/**/!(_)*.scss')
    .pipe(plumber())
    .pipe(sourcemaps.init())
    .pipe(sass({
      outputStyle: 'nested',
      includePaths: ['node_modules/bootstrap/scss']
    }).on('error', sass.logError))
    .pipe(postcss([autoprefixer(), sorting()]))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('static/css'))

    .pipe(filter('**/*.css'))
    .pipe(rename({suffix: '.min'}))
    .pipe(postcss([nano()]))
    .pipe(sourcemaps.write('.'))
    .pipe(gulp.dest('static/css'))

    .on('end', function () {
      cb();
    });
});


/*
 * Development tasks
 */

// Building
gulp.task('build', function (cb) {
  runSequence(
    'clean',
    [
      'css'
    ],
    cb
  );

  gulp.watch('static/scss/**/*.scss', ['css']);
});

// Default task
gulp.task('default', ['build']);
