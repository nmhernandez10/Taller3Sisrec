const UserTag = require('../models').UserTag;
const User = require('../models').User;
const Tag = require('../models').Tag;


module.exports = {
    getAll(req, res) {
        return UserTag.findAll({
            order: [['createdAt', 'DESC'],],
        }).then((usertags) => res.status(200).send(usertags))
            .catch((error) => res.status(400).send(error));
    },
    get(req, res) {
        return UserTag.findById(req.params.id, { include: [Tag, User] })
            .then((usertag) => {
                if (!usertag) {
                    return res.status(404).send({
                        message: 'UserTag not found',
                    });
                }
                return res.status(200).send(usertag);
            })
            .catch((error) => res.status(400).send(error));
    },
    post(req, res) {
        return UserTag.create({            
            like: req.body.like,
            TagId: req.body.TagId,
            UserId: req.body.UserId
        }).then((usertag) => res.status(201).send(usertag))
            .catch((error) => res.status(400).send(error));
    },
    put(req, res) {
        return UserTag.findById(req.params.id)
            .then((usertag) => {
                if (!usertag) {
                    return res.status(404).send({
                        message: 'UserTag not found',
                    });
                }
                return usertag.update({                    
                    like: req.body.like || tag.like,
                    TagId: req.body.TagId || usertag.TagId,
                    UserId: req.body.UserId || usertag.UserId
                }).then((usertag) => res.status(201).send(usertag))
                    .catch((error) => res.status(400).send(error));
            }).catch((error) => res.status(400).send(error));
    },
    delete(req, res) {
        return UserTag.findById(req.params.id)
            .then((usertag) => {
                if (!usertag) {
                    return res.status(404).send({
                        message: 'UserTag not found',
                    });
                }
                return usertag.destroy()
                    .then((usertag) => res.status(200).send(usertag))
                    .catch((error) => res.status(400).send(error));
            }).catch((error) => res.status(400).send(error));
    },
};