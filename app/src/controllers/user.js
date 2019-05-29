const User = require('../models').User;
const Review = require('../models').Review;
const UserTag = require('../models').UserTag;
const Tag = require('../models').Tag;
const Movie = require('../models').Movie;
const MovieTag = require('../models').MovieTag;

module.exports = {
    getAll(req, res) {
        return User.findAll({
            order: [['createdAt', 'DESC'],],
        }).then((users) => res.status(200).send(users))
            .catch((error) => res.status(400).send(error));
    },
    getByName(req, res) {
        return User.findAll({
            include: [Review, { model: UserTag, include: [Tag] }],
            where: { names: { $iLike: '%' + req.params.names + '%' } },
            limit: 10
        }).then((users) => res.status(200).send(users))
            .catch((error) => res.status(400).send(error));
    },
    getByEmail(req, res) {
        return User.findAll({
            include: [Review, { model: UserTag, include: [Tag] }],
            where: { email: req.params.email }
        }).then((users) => res.status(200).send(users))
            .catch((error) => res.status(400).send(error));
    },
    getByYelpId(req, res) {
        return User.findAll({
            include: [Review, { model: UserTag, include: [Tag] }],
            where: { yelp_id: req.params.yelp_id }
        }).then((users) => res.status(200).send(users))
            .catch((error) => res.status(400).send(error));
    },
    get(req, res) {
        return User.findById(req.params.id, { include: [{ model: Review, include: [{ model: Movie, include: [{ model: MovieTag, include: [Tag] }] }] }, { model: UserTag, include: [Tag] }] })
            .then((user) => {
                if (!user) {
                    return res.status(404).send({
                        message: 'User not found',
                    });
                }
                return res.status(200).send(user);
            }).catch((error) => res.status(400).send(error));
    },
    getForProfile(req, res) {
        return User.findById(req.params.id, { include: [{ model: UserTag, include: [Tag] }] })
            .then((user) => {
                if (!user) {
                    return res.status(404).send({
                        message: 'User not found',
                    });
                }
                return res.status(200).send(user);
            }).catch((error) => res.status(400).send(error));
    },
    getAllForContent(req, res) {
        return User.findAll({ include: [{ model: UserTag, include: [Tag] }, Review], where: { content_updated: false } })
            .then(users => res.status(200).send(users)).catch((error) => res.status(400).send(error));
    },
    getForSVD(req, res) {
        return User.findById(req.params.id, { include: [Review] })
            .then((user) => {
                if (!user) {
                    return res.status(404).send({
                        message: 'User not found',
                    });
                }
                return res.status(200).send(user);
            }).catch((error) => res.status(400).send(error));
    },
    getNumUsers(req, res) {
        return User.count({}).then(count => res.status(200).send({ result: count })).catch((error) => res.status(400).send(error));
    },
    post(req, res) {
        return User.create({
            names: req.body.names,
            email: req.body.email,
            password: req.body.password,
            image: req.body.image,
            toponto: req.body.toponto,
            topsvd: req.body.topsvd
        }).then((user) => res.status(201).send(user))
            .catch((error) => res.status(400).send(error));
    },
    put(req, res) {
        return User.findById(req.params.id)
            .then((user) => {
                if (!user) {
                    return res.status(404).send({
                        message: 'User not found',
                    });
                }
                return user.update({
                    names: req.body.names || user.names,
                    email: req.body.email || user.email,
                    password: req.body.password || user.password,
                    image: req.body.image || user.image,
                    toponto: req.body.toponto || user.toponto,
                    topsvd: req.body.topsvd || user.topsvd
                })
                    .then((user) => res.status(200).send(user))
                    .catch((error) => res.status(400).send(error));
            });
    },
    delete(req, res) {
        return User.findById(req.params.id)
            .then((user) => {
                if (!user) {
                    return res.status(404).send({
                        message: 'User not found',
                    });
                }
                return user.destroy()
                    .then((user) => res.status(200).send(user))
                    .catch((error) => res.status(400).send(error));
            });
    },
};