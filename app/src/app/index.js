import React, {Component} from 'react';
import {render} from 'react-dom';
import { BrowserRouter,Route, Link, Switch } from "react-router-dom";
import App from './App'

render( <App/>,
   document.getElementById('app'));