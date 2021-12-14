# transfob

Get a transform stream, like `through2.obj()`. Useful for gulp tasks where you want to iterate over files.

``` js
var transfob = require('transfob');

// convert files to JS object
var data = {};

gulp.task( 'data', function() {
  return gulp.src('data/*.md')
    .pipe( transfob( function( file, enc, next ) {
      var basename = path.basename( file.path, path.extname( file.path ) );
      data[ file.path ] = file.contents.toString();
      next( null, file );
    }) );
});
```
