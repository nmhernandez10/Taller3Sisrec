'use strict';

var Sequelize = require('sequelize');

/**
 * Actions summary:
 *
 * removeColumn "actores" from table "Movies"
 * addColumn "actors" to table "Movies"
 *
 **/

var info = {
    "revision": 5,
    "name": "noname",
    "created": "2019-05-27T07:00:09.430Z",
    "comment": ""
};

var migrationCommands = [{
        fn: "removeColumn",
        params: ["Movies", "actores"]
    },
    {
        fn: "addColumn",
        params: [
            "Movies",
            "actors",
            {
                "type": Sequelize.STRING,
                "field": "actors"
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
