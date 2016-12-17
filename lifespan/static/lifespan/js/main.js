requirejs(["bubbleSource", "jquery", "bubble"], function(bubbleSource, $, bubble) {

  /**
   * function used by the animation method to draw and update the canvas.
   */
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

  /**
   * This method will normalize all the rates that are currently selected.
   * The min and max rate normalizations are used to cap the values.
   *
   * We invert the normalized BirthRate as cordinates 0,0 are at the top left
   * of the canvas, not the bottom left.
   */
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

  /**
   * Setup function adding four bubble sources to the bubble source array.
   */
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

  /**
   * Re creates a bubble source at the given index,
   * @param index the index the bubble source should be recreated at.
   * @param name the name of the bubble used to display when debugging
   * @param birthrate the non-normalized birth rate
   * @param lifeExpectancy the non-normalized life expectancy
   */
  function recreateBubbleSource(index, name, birthrate, lifeExpectancy){
    var b = new bubbleSource(0, canvas.height-50, canvas.height-50, name, birthrate, lifeExpectancy, context, "#FFF", 1);
    bubbleSources[index] = b;
    b.active = true;
    renormalizeSource();
  }

  /**
   * Makes an ajax call to get the birthrate and life expectancy for 
   * the selected country and year
   * @param index the index of the bubble to get the information for
   * @param selectorId the class of the select options, 
   *                   used to get the country and rates. 
   *                   Expected to be selector-\d{1}.
   */
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

  /**
   * Returns the css selector for the country select element.
   * @param selectorId the class of the select options.
   */
  function getCountrySelector(selectorId) {
    return selectorId+'.country-selector';
  }

  /**
   * Returns the css selector for the year select element.
   * @param selectorId the class of the select options.
   */
  function getYearSelector(selectorId) {
    return selectorId+'.year-selector';
  }

  /**
   * Returns the country code selected from country dropdown.
   * @param selectorId the class of the select options.
   */
  function getCountryCode(selectorId) {
    return $(selectorId+'.country-selector').val();
  }

  /**
   * Returns the year selected from the year dropdown.
   * @param selectorId the class of the select options.
   */
  function getYear(selectorId) {
    return $(selectorId+'.year-selector').val();
  }

  /**
   * Returns the index of the bubble source this selector class refers to.
   * @param selectorId the class of the select options.
   */
  function getIndex(selectorId) {
    return selectorId.replace('.selector-','') - 1;
  }

  /**
   * Updates the list of years in the dropdown menu.
   * @param selectorId the class of the select options.
   */
  function updateDateSelector(selectorId) {
    var countryCode = getCountryCode(selectorId);
    var yearSelector = getYearSelector(selectorId);
    var url = 'country/' + countryCode + '/dates';
    $(yearSelector).find('option').remove().end();
    $.getJSON(url, function(json){
      $(yearSelector).append("<option value=''>Select a year</option>");
      $.each(json, function(index) {
            $(yearSelector).append("<option value='"+json[index].date+"'>"+json[index].date+"</option>");
        });
    });
  }

  /**
   * Populates the selector dropdown with the list of countries.
   * @param selectorId the class used to identify the selector dropdowns
   */
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

  /**
   * Animation function used to draw and update the 2d canvas.
   * Calls itself via the requestAnimFrame method.
   */
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

  //Changes to the country dropdown should update the date seletor
  $('.country-selector').change(function() {
    var clazz = $(this).attr('class');
    updateDateSelector('.'+clazz.replace(' country-selector',''));
  });

  //Changes to the date selector should update the bubble sources.
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