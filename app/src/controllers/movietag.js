const MovieTag = require('../models').MovieTag;
const Movie = require('../models').Movie;
const Tag = require('../models').Tag;


module.exports = {
    getAll(req, res) {
        return MovieTag.findAll({
            order: [['createdAt', 'DESC'],],
        }).then((movietags) => res.status(200).send(movietags))
            .catch((error) => res.status(400).send(error));
    },
    get(req, res) {
        return MovieTag.findById(req.params.id, { include: [Tag, Movie] })
            .then((movietag) => {
                if (!movietag) {
                    return res.status(404).send({
                        message: 'MovieTag not found',
                    });
                }
                return res.status(200).send(movietag);
            })
            .catch((error) => res.status(400).send(error));
    },
    post(req, res) {
        return MovieTag.create({
            TagId: req.body.TagId,
            MovieId: req.body.MovieId
        }).then((movietag) => res.status(201).send(movietag))
            .catch((error) => {
                console.log(error);
                return res.status(400).send(error)
            });
    },
    put(req, res) {
        return MovieTag.findById(req.params.id)
            .then((movietag) => {
                if (!movietag) {
                    return res.status(404).send({
                        message: 'MovieTag not found',
                    });
                }
                return movietag.update({
                    TagId: req.body.TagId || movietag.TagId,
                    MovieId: req.body.MovieId || movietag.MovieId
                }).then((movietag) => res.status(201).send(movietag))
                    .catch((error) => res.status(400).send(error));
            }).catch((error) => res.status(400).send(error));
    },
    delete(req, res) {
        return MovieTag.findById(req.params.id)
            .then((movietag) => {
                if (!movietag) {
                    return res.status(404).send({
                        message: 'MovieTag not found',
                    });
                }
                return movietag.destroy()
                    .then((movietag) => res.status(200).send(movietag))
                    .catch((error) => res.status(400).send(error));
            }).catch((error) => res.status(400).send(error));
    },
};