var express = require('express');
var router = express.Router();
const userController = require('../controllers/user');
const movieController = require('../controllers/movie');
const reviewController = require('../controllers/review');
const tagController = require('../controllers/tag');
const movietagController = require('../controllers/movietag');
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

// Movie
router.get('/api/movie/', movieController.getAll);
router.get('/api/movie/:id', movieController.get);
router.post('/api/movie/', movieController.post);
router.put('/api/movie/:id', movieController.put);
router.delete('/api/movie/:id', movieController.delete);
router.get('/api/movie/byname/:name', movieController.getByName);
router.get('/api/movie/byyelpid/:yelp_id', movieController.getByYelpId);
router.get('/api/user/:id/top', movieController.getTop);
router.get('/api/user/:id/toponto', movieController.getTopOnto);
router.get('/api/user/:id/topsvd', movieController.getTopSVD);
//We put 'put' because we needed to send a body request for searching movies by attributes
router.put('/api/movie/byattributes/name', movieController.getByNameAndExactlyByAttributes);
router.put('/api/movie/byattributes/and', movieController.getExactlyByAttributes);
router.put('/api/movie/byattributes/or', movieController.getByAttributes);
router.get('/api/movie/formodel/foronto/:id', movieController.getForOnto);


// Review
router.get('/api/review/', reviewController.getAll);
router.get('/api/review/:id', reviewController.get);
router.post('/api/review/', reviewController.post);
router.put('/api/review/:id', reviewController.putById);
router.put('/api/review/', reviewController.put);
router.delete('/api/review/:id', reviewController.delete);
router.get('/api/review/formodel/forsvd/', reviewController.getAllForSVD);
router.get('/api/review/formodel/forsvdonline/', reviewController.getForOnline);

// Tag
router.get('/api/tag/', tagController.getAll);
router.get('/api/tag/:id', tagController.get);
router.post('/api/tag/', tagController.post);
router.put('/api/tag/:id', tagController.put);
router.delete('/api/tag/:id', tagController.delete);
router.get('/api/tag/byname/:name', tagController.getByName);
router.get('/api/tagnames/',tagController.getNames);

// MovieTag
router.get('/api/movietag/', movietagController.getAll);
router.get('/api/movietag/:id', movietagController.get);
router.post('/api/movietag/', movietagController.post);
router.put('/api/movietag/:id', movietagController.put);
router.delete('/api/movietag/:id', movietagController.delete);

// UserTag
router.get('/api/usertag/', usertagController.getAll);
router.get('/api/usertag/:id', usertagController.get);
router.post('/api/usertag/', usertagController.post);
router.put('/api/usertag/:id', usertagController.put);
router.delete('/api/usertag/:id', usertagController.delete);

module.exports = router;