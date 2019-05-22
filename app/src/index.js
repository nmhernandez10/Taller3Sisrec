// Archivo nodejs-express para inicializar servidor

// Variables y constantes

const express = require('express');
const morgan = require('morgan');
const path = require('path');
const indexRouter = require('./routes/index');
const app = express();

// Settings

app.set('port', process.env.PORT || 8080);
app.set('host', process.env.HOST || '0.0.0.0');

// Middlewares

app.use(morgan('tiny'));
app.use(express.json());

// Routes

app.use('/', indexRouter);

//Static files

app.use(express.static(path.join(__dirname,'public')));
app.use("/:anything",express.static(path.join(__dirname,'public')));

app.listen(app.get('port'),app.get('host'),()=>{
  console.log('Server on port '+app.get('port') + " on host " + app.get('host'));
});