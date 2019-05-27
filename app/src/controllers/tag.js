const Tag = require('../models').Tag;
const UserTag = require('../models').UserTag;
const MovieTag = require('../models').MovieTag;

module.exports = {
    getAll(req, res) {
        return Tag.findAll({
            order: [['createdAt', 'DESC'],],
        }).then((tags) => res.status(200).send(tags))
            .catch((error) => res.status(400).send(error));
    },
    getNames(req, res) {
        return Tag.findAll({
            attributes: ['id','name']
        }).then((tags) => res.status(200).send(tags))
            .catch((error) => res.status(400).send(error));
    },
    getByName(req, res) {
        return Tag.findAll({
            //include: [UserTag, MovieTag],
            where: { name: { $iLike: '%' + req.params.name + '%' } },
            limit: 10
        }).then((tags) => res.status(200).send(tags))
            .catch((error) => res.status(400).send(error));
    },
    get(req, res) {
        return Tag.findById(req.params.id, { include: [UserTag, MovieTag] })
            .then((tag) => {
                if (!tag) {
                    return res.status(404).send({
                        message: 'Tag not found',
                    });
                }
                return res.status(200).send(tag);
            }).catch((error) => res.status(400).send(error));
    },
    post(req, res) {
        return Tag.create({
            name: req.body.name
        }).then((tag) => res.status(201).send(tag))
            .catch((error) => {
                console.log(error);
                return res.status(400).send(error)
            });
    },
    put(req, res) {
        return Tag.findById(req.params.id)
            .then((tag) => {
                if (!tag) {
                    return res.status(404).send({
                        message: 'Tag not found',
                    });
                }
                return tag.update({
                    name: req.body.name || tag.name
                })
                    .then((tag) => res.status(200).send(tag))
                    .catch((error) => res.status(400).send(error));
            });
    },
    delete(req, res) {
        return Tag.findById(req.params.id)
            .then((tag) => {
                if (!tag) {
                    return res.status(404).send({
                        message: 'Tag not found',
                    });
                }
                return tag.destroy()
                    .then((tag) => res.status(200).send(tag))
                    .catch((error) => res.status(400).send(error));
            });
    },
};