'use strict';
var strikePCR = function () {};
var priceChangeStatus = function () {};
var oiChangeStatus = function () {};

// calculate Strike price Put Call Ratio (Put Open Interest/ Call Open Interest)
strikePCR.prototype.parse = function (optionRow) {
    let strikePCR = 0;
    let callOI = optionRow.call.OI.replace(/\,/g,"");
    let putOI = optionRow.call.OI.replace(/\,/g,"");

    
    if ((!isNan(callOI)) && (!isNaN(putOI))) {
        strikePCR = putOI/callOI;
    }
    return strikePCR;
};

function changeStatus(input) {
    let UP = "UP";
    let DOWN = "DOWN";
    let result = "NA"
    if (!isNaN(input)) {
        if (input > 0) {
            result = UP;
        } else {
            result = DOWN;
        }
    }
    return result;
}

priceChangeStatus.prototype.parse = function(optionRow) {
    let CALL = "callPriceChangeStatus";
    let PUT = "putPriceChangeStatus";
    let callNetChange = optionRow.call["Net Chng"].replace(/\,/g,"");;
    let putNetChange = optionRow.put["Net Chng"].replace(/\,/g,"");

    return { CALL : changeStatus(callNetChange), PUT : changeStatus(putNetChange) };
};

oiChangeStatus.prototype.parse = function(optionRow) {
    let CALL = "callOIChangeStatus";
    let PUT = "putOIChangeStatus";
    let callOIChange = optionRow.call["Chng in OI"].replace(/\,/g,"");;
    let putOIChange = optionRow.put["Chng in OI"].replace(/\,/g,"");
    
    return { CALL : changeStatus(callOIChange), PUT : changeStatus(putOIChange) };
};

// CALL
// K7 Net Chng
// J7 Chng in OI
// =IF(AND(K7<0,J7<0),"Long Liquidation",IF(AND(K7<0,J7>0),"Short Buildup",IF(AND(K7>0,J7>0),"Long Buildup",IF(AND(K7>0,J7<0),"Short covering"))))
// O7 = Next Chng
// P7 = Chng in OI
//=IF(AND(O7<0,P7<0),"Long Liquidation",IF(AND(O7<0,P7>0),"Short Buildup",IF(AND(O7>0,P7>0),"Long Buildup",IF(AND(O7>0,P7<0),"Short covering"))))

function strikeChangeInterpretation(netChange, OIChange) {
    let priceChange = 
}
