const http = require('http')
const database = require('./database')

http.createServer(async (req, res)=> {
    // THIS IS FOR CORS ERRORS
    res.setHeader('Access-Control-Allow-Origin', '*'); /* @dev First, read about security */
    res.setHeader('Access-Control-Allow-Methods', 'OPTIONS, GET');
    res.setHeader('Access-Control-Max-Age', 2592000); // 30 days
    if(req.url == '/api/conversations'){
        try {
            res.writeHead(200, {'Content-Type':'application/json'});
            const dataset = await database.conversations(); // here we get the string json
            res.write(dataset); // whoever requests will get the string json as response
        }
        finally {
            res.end(); // must end response. DONT FORGET
        }
    }
}).listen(4000);
// the server will listen to all request in port 400 because
// reactjs is run on port 3000. react will request for data from port
// 3000 to our nodejs in port 4000

