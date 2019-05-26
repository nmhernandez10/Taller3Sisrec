'use strict';
module.exports = (sequelize, DataTypes) => {
  const Movie = sequelize.define('Movie', {
    name: DataTypes.STRING,
    year: DataTypes.STRING,
    photo: DataTypes.STRING,
    director: DataTypes.STRING,
    actores: DataTypes.STRING
  }, {});
  Movie.associate = function (models) {    
    models.Movie.hasMany(models.Review);
    models.Movie.hasMany(models.MovieTag);
  };
  return Movie;
};