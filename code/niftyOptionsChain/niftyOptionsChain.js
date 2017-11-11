'use strict';
const axios = require('axios');
const niftyOptionsScraper = require('../niftyOptionsScraper/src/index.js');
const util = require('util');
const argv = require('yargs').argv
const moment = require('moment');

//default nse symbol
let symbol = "NIFTY";
//default option end date
let expiryDate = "31AUG2017";

if (argv.symbol) {
   symbol = argv.symbol;
}

if (argv.expiryDate) {
  if (moment(argv.expiryDate,"DDMMMYYYY").isValid()) {
     expiryDate = argv.expiryDate;
  } else {
     console.log("expiry date is invalid ");
  }
}
// base url for option from NSE
let base_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/option_chain/optionKeys.jsp?symbol=%s&date=%s';
// construct the url
let get_url = util.format(base_url,symbol,expiryDate);

axios.get(get_url).then( (response) => {
    let today = new Date();
    let date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();    

    let retData = niftyOptionsScraper.parse(response.data);
    retData["metadata"]["optionsInfo"] =  {
       "url" : get_url,
       "symbol" : symbol+".NS",
       "Expiry Date"   : expiryDate
     };

    return JSON.stringify(retData);

})
.then ( (data) => {
  console.log(JSON.stringify(JSON.parse(data),null,2));
});

