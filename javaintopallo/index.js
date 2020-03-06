const {parseStringPromise} = require("xml2js");


function convertPtsoFeature(ptsoFeature) {
    const timeSeries = ptsoFeature['om:result'][0]['wml2:MeasurementTimeseries'][0];
    const propertyId = timeSeries.$['gml:id'];
    return timeSeries['wml2:point'].map(p => p['wml2:MeasurementTVP'][0]).map(p => ({
        id: propertyId,
        time: p['wml2:time'][0],
        value: p['wml2:value'][0],
    }));
}


async function convertPointXML(xmlString) {
    const data = await parseStringPromise(xmlString);
    const ptsoFeatures = data['wfs:FeatureCollection']['wfs:member'].flatMap(w => w['omso:PointTimeSeriesObservation'] || []);
    return ptsoFeatures.flatMap(convertPtsoFeature);
}

module.exports = {
    convertPointXML,
};
