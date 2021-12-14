
var postcss = require('gulp-postcss');
var { gulp, series, src, dest, watch, paths } = require('gulp');
var autoprefixer = require('autoprefixer');
var cssnano = require('cssnano');
var sass = require('gulp-sass')(require('sass'));
var sortMediaQueries = require('postcss-sort-media-queries');
var purgecss = require('gulp-purgecss');

function style() {
  return src('./_assets/style.scss')
      .pipe(sass().on('error', sass.logError))
      .pipe(postcss([
            sortMediaQueries(),
            autoprefixer(),
            cssnano(),
        ]))
      .pipe(purgecss({
            content: ['./**/*.html.dj'],
            safelist: {
              deep: [/breadcrumb/],
            }
          }))
      .pipe(dest('./_static/css/'));

};

exports.default = series(style)

exports.watch = function() {
  watch('./_assets/style.scss',{ ignoreInitial: false }, style)
}
