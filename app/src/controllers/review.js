const Review = require('../models').Review;
const Movie = require('../models').Movie;
const User = require('../models').User;


module.exports = {
    getAll(req, res) {
        return Review.findAll({
            order: [['createdAt', 'DESC'],],
        }).then((reviews) => res.status(200).send(reviews))
            .catch((error) => res.status(400).send(error));
    },
    getAllForSVD(req, res) {
        return Review.findAll({ include: [User], where: { svd_updated: false } })
            .then(reviews => res.status(200).send(reviews)).catch((error) => res.status(400).send(error));
    },
    get(req, res) {
        return Review.findById(req.params.id, { include: [User, Movie] })
            .then((review) => {
                if (!review) {
                    return res.status(404).send({
                        message: 'Review not found',
                    });
                }
                return res.status(200).send(review);
            })
            .catch((error) => res.status(400).send(error));
    },
    post(req, res) {
        return Review.findAll({
            where: {
                UserId: req.body.UserId,
                MovieId: req.body.MovieId
            }
        }).then(reviews => {
            if (reviews.length > 0) {
                return res.status(404).send({
                    message: 'Review already exists'
                });
            }
            else {
                return Review.create({
                    stars: req.body.stars,
                    date: req.body.date,
                    UserId: req.body.UserId,
                    MovieId: req.body.MovieId,
                    svd_updated: false
                }).then((review) => res.status(201).send(review))
                    .catch((error) => res.status(400).send(error));
            }
        }).catch((error) => res.status(400).send(error));
    },
    put(req, res) {
        return Review.findAll({
            where: {
                UserId: req.body.UserId,
                MovieId: req.body.MovieId
            }
        }).then(reviews => {
            if (reviews.length > 0) {
                return Review.findById(reviews[0].get({ plain: true }).id)
                    .then((review) => {
                        if (!review) {
                            return res.status(404).send({
                                message: 'Review not found',
                            });
                        }
                        return review.update({
                            stars: req.body.stars || review.stars,
                            date: req.body.date || review.date,
                            UserId: req.body.UserId || review.UserId,
                            MovieId: req.body.MovieId || review.MovieId,
                            svd_updated: req.body.svd_updated
                        }).then((review) => res.status(201).send(review))
                            .catch((error) => res.status(400).send(error));
                    }).catch((error) => res.status(400).send(error));
            }
            else {
                return Review.create({
                    stars: req.body.stars,
                    date: req.body.date,
                    UserId: req.body.UserId,
                    MovieId: req.body.MovieId,
                    svd_updated: req.body.svd_updated
                }).then((review) => res.status(201).send(review))
                    .catch((error) => res.status(400).send(error));
            }
        }).catch((error) => res.status(400).send(error));
    },
    putById(req, res) {
        return Review.findById(req.params.id)
            .then((review) => {
                if (!review) {
                    return res.status(404).send({
                        message: 'Review not found',
                    });
                }
                return review.update({
                    stars: req.body.stars || review.stars,
                    date: req.body.date || review.date,
                    UserId: req.body.UserId || review.UserId,
                    MovieId: req.body.MovieId || review.MovieId,
                    svd_updated: req.body.svd_updated
                }).then((review) => res.status(201).send(review))
                    .catch((error) => res.status(400).send(error));
            }).catch((error) => res.status(400).send(error));
    },
    delete(req, res) {
        return Review.findById(className.id)
            .then((review) => {
                if (!review) {
                    return res.status(404).send({
                        message: 'Review not found',
                    });
                }
                return review.destroy()
                    .then((review) => res.status(200).send(review))
                    .catch((error) => res.status(400).send(error));
            }).catch((error) => res.status(400).send(error));
    },
};