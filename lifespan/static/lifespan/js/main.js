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

  function renormalizeSource() {
    maxBirthRate = 0;
    minBirthRate = Number.MAX_VALUE;
    
    maxLifeExpectancy = 0;
    minLifeExpectancy = Number.MAX_VALUE;

    $.each(bubbleSources, function(index, value) {
        value.noramlized = false;
        if(value.birthrate < minBirthRate) {
          minBirthRate = value.birthrate;
        }
        if(value.birthrate > maxBirthRate) {
          maxBirthRate = value.birthrate;
        }
        if(value.lifeExpectancy < minLifeExpectancy) {
          minLifeExpectancy = value.lifeExpectancy;
        }
        if(value.lifeExpectancy > maxLifeExpectancy) {
          maxLifeExpectancy = value.lifeExpectancy;
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

  function addBubbleSources() {
    var b0 = new bubbleSource(95, canvas.height-50, canvas.height-50, "name", 1, 1, context, "#FFF", 1);
    var b1 = new bubbleSource(95, canvas.height-50, canvas.height-50, "name", 1, 1, context, "#FFF", 1);
    var b2 = new bubbleSource(95, canvas.height-50, canvas.height-50, "name", 1, 1, context, "#FFF", 1);
    var b3 = new bubbleSource(95, canvas.height-50, canvas.height-50, "name", 1, 1, context, "#FFF", 1);
    bubbleSources[0] = b0;
    bubbleSources[1] = b1;
    bubbleSources[2] = b2;
    bubbleSources[3] = b3;
  }

  function recreateBubbleSource(index, name, birthrate, lifeExpectancy){
    console.log(index);
    var b = new bubbleSource(0, canvas.height-50, canvas.height-50, name, birthrate, lifeExpectancy, context, "#FFF", 1);
    bubbleSources[index] = b;
    b.active = true;
    renormalizeSource();
  }

  function getBubbleSourceInfo(index, selectorId){
    var countryCode = getCountryCode(selectorId);
    var year = getYear(selectorId);
    var url = 'country/' + countryCode + '/rate?year='+year;

    
    $.getJSON(url, function(json){
      var birthrate;
      var lifeExpectancy;
      $.each(json, function(index) {
        if(json[index].rate_type == "birth"){
          birthrate = json[index].rate;
        }
        if(json[index].rate_type == "lifespan"){
          lifespan = json[index].rate;
        }
      });
      recreateBubbleSource(getIndex(selectorId), countryCode, birthrate, lifespan);
    });
    
  }

  function getCountrySelector(selectorId) {
    return selectorId+'.country-selector';
  }
  function getYearSelector(selectorId){
    return selectorId+'.year-selector';
  }
  function getCountryCode(selectorId) {
    return $(selectorId+'.country-selector').val();
  }
  function getYear(selectorId) {
    return $(selectorId+'.year-selector').val();
  }

  function getIndex(selectorId) {
    return selectorId.replace('.selector-','') - 1;
  }

  function updateDateSelector(selectorId) {
    var countryCode = getCountryCode(selectorId);
    var yearSelector = getYearSelector(selectorId);
    var url = 'country/' + countryCode + '/dates';
    console.log(url);
    $(yearSelector).find('option').remove().end();
    $.getJSON(url, function(json){
      $(yearSelector).append("<option value=''>Select a year</option>");
      $.each(json, function(index) {
            $(yearSelector).append("<option value='"+json[index].date+"'>"+json[index].date+"</option>");
        });
    });
  }

  function populateCountryDropdown(selectorId) {
    var url = 'country';
    var countrySelectorId = getCountrySelector(selectorId);
    $(countrySelectorId).append("<option value=''>Select a country</option>");
    $.getJSON(url, function(json){
      $.each(json, function(index) {
            $(countrySelectorId).append("<option value='"+json[index].country_code+"'>"+json[index].country_name+"</option>");
        });
    });
  }

  function animate() {
    var width = $('.content').width();
    document .getElementById('canvas').setAttribute('width',width);
    var bubbleSpacing = width / (bubbleSources.length);
    $.each(bubbleSources, function(index, value) {
        value.x = (bubbleSpacing *(index+1) - (bubbleSpacing/2));
        value.update();
        value.draw();
    });

    requestAnimFrame(function() {
      animate();
    });
  }

  $('.country-selector').change(function() {
    var clazz = $(this).attr('class');
    updateDateSelector('.'+clazz.replace(' country-selector',''));
  });

  $('.year-selector').change(function() {
    var clazz = $(this).attr('class');
    getBubbleSourceInfo(0,'.'+clazz.replace(' year-selector',''));
  });

  populateCountryDropdown('.selector-1');
  populateCountryDropdown('.selector-2');
  populateCountryDropdown('.selector-3');
  populateCountryDropdown('.selector-4');
  addBubbleSources();
  renormalizeSource();
  animate();

});

require.config({
    paths: {
        jquery: 'libs/jquery-3.1.1.min',
        bubble: 'bubbles/bubble',
        bubbleSource: 'bubbles/bubbleSource'
    }
});