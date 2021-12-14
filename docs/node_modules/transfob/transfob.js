/**
 * transfob
 * get a transform stream, like through2.obj()
 */

var Transform = require('stream').Transform;

module.exports = function transfob( _transform ) {
  var transform = new Transform({
    objectMode: true
  });

  transform._transform = _transform;

  return transform;
};
