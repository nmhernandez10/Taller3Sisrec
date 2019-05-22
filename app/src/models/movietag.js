'use strict';
module.exports = (sequelize, DataTypes) => {
    const MovieTag = sequelize.define('MovieTag', {
    }, {});
    MovieTag.associate = function (models) {
        models.MovieTag.belongsTo(models.Movie, {
            foreignKey: { allowNull: false }
        });
        models.MovieTag.belongsTo(models.Tag, {
            foreignKey: { allowNull: false }
        });
    };
    return MovieTag;
};
