# nseOptionsChain [![Build Status](https://travis-ci.org/ericnorris/striptags.svg)](https://travis-ci.org/ericnorris/striptags)

**Note:** `v3+` targets ES6, and is therefore incompatible with the master branch of `uglifyjs`. You can either:
- use `babili`, which supports ES6
- use the `harmony` branch of `uglifyjs`
- stick with the [2.x.x](https://github.com/ericnorris/striptags/tree/v2.x.x) branch

## Features
- parse the nse options chain and get a json of the option chain

## Installing
```
npm install nseOptionChain
```

## Basic Usage
```javascript
nseOptionChain.parse(html);
```

### Example
```javascript
var nseOptionChain = require('nseOptionChain');

nseOptionChain.parse(html);
```

Outputs:
```
'lorem ipsum dolor sit amet'
```

```
lorem ipsum <strong>dolor</strong> sit amet'
```

```
'<a href="https://example.com">lorem ipsum dolor sit amet</a>'
```

```

lorem ipsum
dolor
 sit amet
```

## Tests
You can run tests (powered by [mocha](http://mochajs.org/)) locally via:
```
npm test
```

Generate test coverage (powered by [istanbul](https://github.com/gotwarlost/istanbul)) via :
```
npm run coverage
```

