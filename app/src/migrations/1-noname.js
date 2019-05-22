'use strict';

var Sequelize = require('sequelize');

/**
 * Actions summary:
 *
 * createTable "Movies", deps: []
 * createTable "Tags", deps: []
 * createTable "Users", deps: []
 * createTable "MovieTags", deps: [Movies, Tags]
 * createTable "Reviews", deps: [Movies, Users]
 * createTable "UserTags", deps: [Tags, Users]
 *
 **/

var info = {
    "revision": 1,
    "name": "noname",
    "created": "2019-05-22T01:46:40.739Z",
    "comment": ""
};

var migrationCommands = [{
        fn: "createTable",
        params: [
            "Movies",
            {
                "id": {
                    "type": Sequelize.INTEGER,
                    "field": "id",
                    "autoIncrement": true,
                    "primaryKey": true,
                    "allowNull": false
                },
                "name": {
                    "type": Sequelize.STRING,
                    "field": "name"
                },
                "year": {
                    "type": Sequelize.STRING,
                    "field": "year"
                },
                "photo": {
                    "type": Sequelize.STRING,
                    "field": "photo"
                },
                "createdAt": {
                    "type": Sequelize.DATE,
                    "field": "createdAt",
                    "allowNull": false
                },
                "updatedAt": {
                    "type": Sequelize.DATE,
                    "field": "updatedAt",
                    "allowNull": false
                }
            },
            {}
        ]
    },
    {
        fn: "createTable",
        params: [
            "Tags",
            {
                "id": {
                    "type": Sequelize.INTEGER,
                    "field": "id",
                    "autoIncrement": true,
                    "primaryKey": true,
                    "allowNull": false
                },
                "name": {
                    "type": Sequelize.STRING,
                    "field": "name"
                },
                "createdAt": {
                    "type": Sequelize.DATE,
                    "field": "createdAt",
                    "allowNull": false
                },
                "updatedAt": {
                    "type": Sequelize.DATE,
                    "field": "updatedAt",
                    "allowNull": false
                }
            },
            {}
        ]
    },
    {
        fn: "createTable",
        params: [
            "Users",
            {
                "id": {
                    "type": Sequelize.INTEGER,
                    "field": "id",
                    "autoIncrement": true,
                    "primaryKey": true,
                    "allowNull": false
                },
                "names": {
                    "type": Sequelize.STRING,
                    "field": "names"
                },
                "email": {
                    "type": Sequelize.STRING,
                    "field": "email",
                    "unique": true
                },
                "password": {
                    "type": Sequelize.STRING,
                    "field": "password"
                },
                "image": {
                    "type": Sequelize.STRING,
                    "field": "image"
                },
                "toponto": {
                    "type": Sequelize.TEXT,
                    "field": "toponto"
                },
                "topsvd": {
                    "type": Sequelize.TEXT,
                    "field": "topsvd"
                },
                "createdAt": {
                    "type": Sequelize.DATE,
                    "field": "createdAt",
                    "allowNull": false
                },
                "updatedAt": {
                    "type": Sequelize.DATE,
                    "field": "updatedAt",
                    "allowNull": false
                }
            },
            {}
        ]
    },
    {
        fn: "createTable",
        params: [
            "MovieTags",
            {
                "id": {
                    "type": Sequelize.INTEGER,
                    "field": "id",
                    "autoIncrement": true,
                    "primaryKey": true,
                    "allowNull": false
                },
                "createdAt": {
                    "type": Sequelize.DATE,
                    "field": "createdAt",
                    "allowNull": false
                },
                "updatedAt": {
                    "type": Sequelize.DATE,
                    "field": "updatedAt",
                    "allowNull": false
                },
                "MovieId": {
                    "type": Sequelize.INTEGER,
                    "field": "MovieId",
                    "onUpdate": "CASCADE",
                    "onDelete": "SET NULL",
                    "references": {
                        "model": "Movies",
                        "key": "id"
                    },
                    "allowNull": true
                },
                "TagId": {
                    "type": Sequelize.INTEGER,
                    "field": "TagId",
                    "onUpdate": "CASCADE",
                    "onDelete": "NO ACTION",
                    "references": {
                        "model": "Tags",
                        "key": "id"
                    },
                    "allowNull": false
                }
            },
            {}
        ]
    },
    {
        fn: "createTable",
        params: [
            "Reviews",
            {
                "id": {
                    "type": Sequelize.INTEGER,
                    "field": "id",
                    "autoIncrement": true,
                    "primaryKey": true,
                    "allowNull": false
                },
                "stars": {
                    "type": Sequelize.INTEGER,
                    "field": "stars"
                },
                "date": {
                    "type": Sequelize.DATE,
                    "field": "date"
                },
                "svd_updated": {
                    "type": Sequelize.BOOLEAN,
                    "field": "svd_updated"
                },
                "createdAt": {
                    "type": Sequelize.DATE,
                    "field": "createdAt",
                    "allowNull": false
                },
                "updatedAt": {
                    "type": Sequelize.DATE,
                    "field": "updatedAt",
                    "allowNull": false
                },
                "MovieId": {
                    "type": Sequelize.INTEGER,
                    "field": "MovieId",
                    "onUpdate": "CASCADE",
                    "onDelete": "SET NULL",
                    "references": {
                        "model": "Movies",
                        "key": "id"
                    },
                    "allowNull": true
                },
                "UserId": {
                    "type": Sequelize.INTEGER,
                    "field": "UserId",
                    "onUpdate": "CASCADE",
                    "onDelete": "NO ACTION",
                    "references": {
                        "model": "Users",
                        "key": "id"
                    },
                    "allowNull": false
                }
            },
            {}
        ]
    },
    {
        fn: "createTable",
        params: [
            "UserTags",
            {
                "id": {
                    "type": Sequelize.INTEGER,
                    "field": "id",
                    "autoIncrement": true,
                    "primaryKey": true,
                    "allowNull": false
                },
                "like": {
                    "type": Sequelize.BOOLEAN,
                    "field": "like"
                },
                "createdAt": {
                    "type": Sequelize.DATE,
                    "field": "createdAt",
                    "allowNull": false
                },
                "updatedAt": {
                    "type": Sequelize.DATE,
                    "field": "updatedAt",
                    "allowNull": false
                },
                "TagId": {
                    "type": Sequelize.INTEGER,
                    "field": "TagId",
                    "onUpdate": "CASCADE",
                    "onDelete": "SET NULL",
                    "references": {
                        "model": "Tags",
                        "key": "id"
                    },
                    "allowNull": true
                },
                "UserId": {
                    "type": Sequelize.INTEGER,
                    "field": "UserId",
                    "onUpdate": "CASCADE",
                    "onDelete": "SET NULL",
                    "references": {
                        "model": "Users",
                        "key": "id"
                    },
                    "allowNull": true
                }
            },
            {}
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
