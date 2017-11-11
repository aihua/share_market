'use strict';
const cheerio = require('cheerio');
const cheerioTableparser = require('cheerio-tableparser');
const striptags = require('striptags');
 
var niftyOptionsScraper = function () {};

niftyOptionsScraper.prototype.parse = function (html) {

       let today = new Date();
       let date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
       let time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();    
       let metadata = { 
          "NiftyOptionChainScraper": {
              "script" : "NiftyOptionsScraper", 
	      "version" : "0.1",
              "date":date, 
              "time":time
           },
       };
       // extract the table required
       let optionChain = extractOptionsChain(html);
       //convert it to json
       let obj = convertToJson(optionChain.data, optionChain.numRows, optionChain.header, optionChain.strikePriceIndex);
       let retObj = { "data" : obj, "metadata" : metadata } ;
       return JSON.parse(JSON.stringify(retObj));
};

function convertToJson(data, numRows, header, strikePriceIndex) {
      let jsonOption = {};
      for(let j=0; j<numRows; j++) {
         var newObj = new Object();
         var call = new Object();
         var put  = new Object();
         for (let i =0; i<header.length; i++) {
            if (i == strikePriceIndex) {
               newObj[header[i]] = data[i][j];
            } else if ( i < strikePriceIndex) {
               call[header[i]] = data[i][j];
            } else {
               put[header[i]] = data[i][j];
            }
         }
         newObj["call"]= call;
         newObj["put"] = put;
         if (data[strikePriceIndex][j] != "") {
            jsonOption[data[strikePriceIndex][j]] =  newObj;
         }
      }
      return (jsonOption);
}

function extractOptionsChain(respData) {
      let strikePriceIndex = -1;
      let STRIKE_PRICE = "Strike Price";
      let numRows = -1;
      let header = [];

      let $ = cheerio.load(respData);
      let data = [];
      cheerioTableparser($);
      data = $("#octable").parsetable();
      // remove the first column
      data.splice(0,1);
      // remove the last column
      data.splice(data.length -1 ,1);
      //clean the data and get the strike price index
      for(let i = 0; i < data.length; i++) {
         //remove the first item
         data[i].splice(0,1);
         if (data[i][0] == STRIKE_PRICE) {
            strikePriceIndex = i;
         }
         header.push(striptags(data[i][0]));
         // remove the header   
         data[i].splice(0,1);
         if (numRows == -1 ) {
            numRows = data[i].length ;
         } else if (numRows != data[i].length) {
            console.log("Rows mismatch");
         }
         for(let j = 0; j < data[i].length; j++) {
            data[i][j] = striptags(data[i][j]);
            data[i][j] = data[i][j].toString().replace(/\t/g,'');
            data[i][j] = data[i][j].toString().replace(/\n/g,'');
            data[i][j] = data[i][j].toString().replace(/\n/g,'').trim();
         }
      }
      return {
         data: data,
	   numRows : numRows,
	   strikePriceIndex: strikePriceIndex,
	   header: header
      }
}

module.exports = new niftyOptionsScraper();
