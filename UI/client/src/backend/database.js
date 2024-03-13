const {MongoClient} = require("mongodb");
const uri = "mongodb://0.0.0.0:27017";

const client = new MongoClient(uri);
client.connect()

async function conversations(){
    try {
        const data = await client.db('ResearchAssist').collection('ra_conversation').find().toArray();
        return JSON.stringify(data);
    }
    catch{
        console.log("DB Closed");
        await client.close();
    }
}

module.exports = {conversations};
