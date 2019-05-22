'use strict';
module.exports = (sequelize, DataTypes) => {
  const User = sequelize.define('User', {
    names: DataTypes.STRING,
    email: { type: DataTypes.STRING, unique: true },
    password: DataTypes.STRING,
    image: DataTypes.STRING,
    toponto: DataTypes.TEXT,
    topsvd : DataTypes.TEXT
  }, {});
  User.associate = function (models) {
    models.User.hasMany(models.Review);
    models.User.hasMany(models.UserTag);
  };
  return User;
};