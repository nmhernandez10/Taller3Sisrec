const neo4j = require('neo4j-driver').v1;
const fs = require('fs');

console.log('Starting extraction');

let user = "neo4j";
let password = "team8sisrec";
let uri = "bolt://localhost:7687";

const numMovies = 193886;

extract = async (id) => {
    const driver = neo4j.driver(uri, neo4j.auth.basic(user, password));
    const session = driver.session();
    const resultPromise = session.run(
        'MATCH p=(m)-[]->()-[:MyMovie]->(r) WHERE m:Movie AND m.id = "' + id + '"RETURN m, r',
        {}
    );

    let data = [];

    await resultPromise.then(result => {
        session.close();
        for (let record of result.records) {
            data.push(record._fields[1].properties.id);
        }

        if (id % 1000 === 0) {
            console.log(id * 100 / numMovies + ' %');
        }

        driver.close();
    });

    return data;
}

extract_all = async () => {

    console.log('Extracting...');

    let data = {};

    for (let i = 1; i <= numMovies; i++) {
        data[i] = await extract(i);
    }

    let datajson = JSON.stringify(data);
    fs.writeFileSync('graph.json', datajson);

    console.log('Finished');
}

extract_all();