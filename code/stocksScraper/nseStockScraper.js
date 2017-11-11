'use strict';
const axios = require('axios');
const util = require('util');
const argv = require('yargs').argv
const moment = require('moment');

//default nse symbol
let symbol = "INFY.NS";
//duration DDMMMYYYY
let startDate = moment("20170101","YYYYMMDD");
let endDate = moment();
let period = "d";

if (argv.symbol) {
   symbol = argv.symbol;
}

if (argv.startDate) {
  if (moment(argv.startDate,"YYYYMMDD").isValid()) {
    startDate = argv.startDate;
  } else {
     console.log("start date is invalid ");
     process.exit(1);
  }
}

if (argv.endDate) {
    if (moment(argv.endDate,"YYYYMMDD").isValid()) {
        endDate = argv.endDate;
    } else {
       console.log("end date is invalid ");
       process.exit(1);
    }
}

if (argv.period) {
    if ((argv.period == "m") || (argv.period == "M")) {
        period = "mo";
    }
}

startDate = moment(startDate,"YYYYMMDD").unix();
endDate = moment(endDate,"  YYYYMMDD").unix();

if (endDate < startDate) {
    console.log("Invalid: End Date is earlier that Start Date");
    process.exit(1);
}
// base url for option from NSE
let base_url = 'https://query2.finance.yahoo.com/v8/finance/chart/%s?&lang=en-IN&region=IN&period1=%s&period2=%s&interval=1%s';
// construct the url
let get_url = util.format(base_url ,symbol ,startDate ,endDate,period);

axios.get(get_url).then( (response) => {
    console.log( JSON.stringify(response.data));
});

