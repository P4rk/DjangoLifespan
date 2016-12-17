This projects demonstrates the integration of a third party API, the [world bank api](http://data.worldbank.org/developers). It is used to list all available countries, there birth rates and life expectancies. A python library integration with this API already exists and was not used ([wbdata](https://github.com/OliverSherouse/wbdata)). 

The frontend of this project is pure js and html 5 canvas. The only libraries used were JQuery and require.js. If anything more complicated than this was to be constructed I would most likely move it to the [D3 Library](https://github.com/d3).

#Running tests
```
./manage.py test
```
#Running coverage
```
coverage run ./manage.py test && coverage report -m
```
