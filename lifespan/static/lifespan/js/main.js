requirejs(["bubbleSource", "jquery", "bubble"], function(bubbleSource, $, bubble) {
  window.requestAnimFrame = (function(callback) {
    return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
      function(callback) {
        window.setTimeout(callback, 500 / 60);
      };
  })();


  var canvas = document.getElementById('canvas');
  var context = canvas.getContext('2d');
  var bubbleSources = [];

  minLifeExpectancyNormalization = 0.3;
  maxLifeExpectancyNormalization = 0.8;
   
  minBirthRateNormalization = 0.1;
  maxBirthRateNormalization = 0.9;


  function addBubbleSource() {
    var b = new bubbleSource(95, canvas.height-50, canvas.height-50, "name", 1, 1, context, "#FFF", 1);
    bubbleSources[bubbleSources.length] = b;
  }

  function renormalizeSource() {
    maxBirthRate = 0;
    minBirthRate = Number.MAX_VALUE;
    
    maxLifeExpectancy = 0;
    minLifeExpectancy = Number.MAX_VALUE;

    $.each(bubbleSources, function(index, value) {
      value.noramlized = false;
      if(value._birthrate < minBirthRate) {
        minBirthRate = value._birthrate;
      }
      if(value._birthrate > maxBirthRate) {
        maxBirthRate = value._birthrate;
      }
      if(value._lifeExpectancy < minLifeExpectancy) {
        minLifeExpectancy = value._lifeExpectancy;
      }
      if(value._lifeExpectancy > maxLifeExpectancy) {
        maxLifeExpectancy = value._lifeExpectancy;
      }
    });
    $.each(bubbleSources, function(index, value) {

      invertedNormalizedBirthRate = minBirthRateNormalization + ((value.birthrate-maxBirthRate)*(maxBirthRateNormalization - minBirthRateNormalization))/(minBirthRate-maxBirthRate);
      normalizedlifeExpectancy = minLifeExpectancyNormalization + ((value.lifeExpectancy-minLifeExpectancy)*(maxLifeExpectancyNormalization-minLifeExpectancyNormalization)/(maxLifeExpectancy-minLifeExpectancy));
      value.normalizedLifeExpectancy = normalizedlifeExpectancy;
      value.normalizedBirthrate = invertedNormalizedBirthRate;

      value.noramlized = true;
    });
  }

  function animate() {
    var width = $('.content').width();
    document .getElementById('canvas').setAttribute('width',width);
    $.each(bubbleSources, function(index, value) {
      value.update();
      value.draw();
    });

    requestAnimFrame(function() {
      animate();
    });
  }
  addBubbleSource();
  renormalizeSource();
  animate();

});

require.config({
    paths: {
        jquery: 'libs/jquery-3.1.1.slim.min',
        bubble: 'bubbles/bubble',
        bubbleSource: 'bubbles/bubbleSource'
    }
});