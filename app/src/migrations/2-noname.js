'use strict';

var Sequelize = require('sequelize');

/**
 * Actions summary:
 *
 * addColumn "actores" to table "Movies"
 * addColumn "director" to table "Movies"
 *
 **/

var info = {
    "revision": 2,
    "name": "noname",
    "created": "2019-05-25T00:45:20.807Z",
    "comment": ""
};

var migrationCommands = [{
        fn: "addColumn",
        params: [
            "Movies",
            "actores",
            {
                "type": Sequelize.STRING,
                "field": "actores"
            }
        ]
    },
    {
        fn: "addColumn",
        params: [
            "Movies",
            "director",
            {
                "type": Sequelize.STRING,
                "field": "director"
            }
        ]
    }
];

module.exports = {
    pos: 0,
    up: function(queryInterface, Sequelize)
    {
        var index = this.pos;
        return new Promise(function(resolve, reject) {
            function next() {
                if (index < migrationCommands.length)
                {
                    let command = migrationCommands[index];
                    console.log("[#"+index+"] execute: " + command.fn);
                    index++;
                    queryInterface[command.fn].apply(queryInterface, command.params).then(next, reject);
                }
                else
                    resolve();
            }
            next();
        });
    },
    info: info
};
