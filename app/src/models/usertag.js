'use strict';
module.exports = (sequelize, DataTypes) => {
    const UserTag = sequelize.define('UserTag', {        
        like: DataTypes.BOOLEAN
    }, {});
    UserTag.associate = function (models) {
        models.UserTag.belongsTo(models.User, {
            foreignKey: { allowNull: false }
        });
        models.UserTag.belongsTo(models.Tag, {
            foreignKey: { allowNull: false }
        });
    };
    return UserTag;
};
