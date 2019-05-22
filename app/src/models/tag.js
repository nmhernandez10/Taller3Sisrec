'use strict';
module.exports = (sequelize, DataTypes) => {
    const Tag = sequelize.define('Tag', {
        name: DataTypes.STRING
    }, {});
    Tag.associate = function (models) {
        models.Tag.hasMany(models.MovieTag);
        models.Tag.hasMany(models.UserTag);
    };
    return Tag;
};