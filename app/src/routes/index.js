var express = require('express');
var router = express.Router();
const userController = require('../controllers/user');
const businessController = require('../controllers/business');
const photoController = require('../controllers/photo');
const reviewController = require('../controllers/review');
const tagController = require('../controllers/tag');
const businesstagController = require('../controllers/businesstag');
const usertagController = require('../controllers/usertag');

// Static files on index.js of app will render front

// User
router.get('/api/user/', userController.getAll);
router.get('/api/user/:id', userController.get);
router.get('/api/user/bynames/:names', userController.getByName);
router.get('/api/user/byemail/:email', userController.getByEmail);
router.get('/api/user/byyelpid/:yelp_id', userController.getByYelpId);
router.post('/api/user/', userController.post);
router.put('/api/user/:id', userController.put);
router.delete('/api/user/:id', userController.delete);
router.get('/api/user/formodel/forcontent/', userController.getAllForContent);
router.get('/api/user/formodel/forsvd/:id', userController.getForSVD);
router.get('/api/user/formodel/count/', userController.getNumUsers);
router.get('/api/user/forprofile/:id', userController.getForProfile);

// Business
router.get('/api/business/', businessController.getAll);
router.get('/api/business/:id', businessController.get);
router.post('/api/business/', businessController.post);
router.put('/api/business/:id', businessController.put);
router.delete('/api/business/:id', businessController.delete);
router.get('/api/business/byname/:name', businessController.getByName);
router.get('/api/business/byyelpid/:yelp_id', businessController.getByYelpId);
router.get('/api/user/:id/top', businessController.getTop);
//We put 'put' because we needed to send a body request for searching businesses by attributes
router.put('/api/business/byattributes/name', businessController.getByNameAndExactlyByAttributes);
router.put('/api/business/byattributes/and', businessController.getExactlyByAttributes);
router.put('/api/business/byattributes/or', businessController.getByAttributes);

// Photo
router.get('/api/business/:business_id/photo/', photoController.getAll);
router.get('/api/business/:business_id/photo/:id', photoController.get);
router.post('/api/business/:business_id/photo/', photoController.post);
router.put('/api/business/:business_id/photo/:id', photoController.put);
router.delete('/api/business/:business_id/photo/:id', photoController.delete);

// Review
router.get('/api/review/', reviewController.getAll);
router.get('/api/review/:id', reviewController.get);
router.post('/api/review/', reviewController.post);
router.put('/api/review/:id', reviewController.putById);
router.put('/api/review/', reviewController.put);
router.delete('/api/review/:id', reviewController.delete);
router.get('/api/review/formodel/forsvd/', reviewController.getAllForSVD);

// Tag
router.get('/api/tag/', tagController.getAll);
router.get('/api/tag/:id', tagController.get);
router.post('/api/tag/', tagController.post);
router.put('/api/tag/:id', tagController.put);
router.delete('/api/tag/:id', tagController.delete);
router.get('/api/tag/byname/:name', tagController.getByName);
router.get('/api/tagnames/',tagController.getNames);

// BusinessTag
router.get('/api/businesstag/', businesstagController.getAll);
router.get('/api/businesstag/:id', businesstagController.get);
router.post('/api/businesstag/', businesstagController.post);
router.put('/api/businesstag/:id', businesstagController.put);
router.delete('/api/businesstag/:id', businesstagController.delete);

// UserTag
router.get('/api/usertag/', usertagController.getAll);
router.get('/api/usertag/:id', usertagController.get);
router.post('/api/usertag/', usertagController.post);
router.put('/api/usertag/:id', usertagController.put);
router.delete('/api/usertag/:id', usertagController.delete);

module.exports = router;