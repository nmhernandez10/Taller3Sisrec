'use strict';
module.exports = (sequelize, DataTypes) => {
    const Review = sequelize.define('Review', {
        stars: DataTypes.REAL,
        date: DataTypes.DATE,
        svd_updated: DataTypes.BOOLEAN
    }, {});
    Review.associate = function(models) {
        models.Review.belongsTo(models.User,{
            foreignKey: {allowNull: false}
            });        
        models.Review.belongsTo(models.Movie,{
            foreignKey: {allowNull: false}
            });        
    };
    return Review;
};
