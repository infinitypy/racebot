const dgdata = require('./index.js');
console.log('starting tests');

let url = 'https://static-api.nkstatic.com/appdocs/11/dailyChallenges/841';
// this website is in bytes, but because you are viewing it in a browser you see weird text. That is what { encoding : null } is for
request(url, { encoding: null }, (err, res, body) => {
    if (err) {
        throw new Error('there was an issue with the tester fetching the url');
    }
    let g = dgdata.decode(body).substr(14).toString('utf-8');
});