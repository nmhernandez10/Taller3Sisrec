import React, {Component} from 'react';
import {render} from 'react-dom';
import { BrowserRouter,Route, Link, Switch } from "react-router-dom";

import Session from './private/Session'
import App from './public/App'
import LogIn from './public/LogIn'
import SignUp from './public/SignUp'
import Profile from './private/Profile'

render(
    <BrowserRouter>
        <Switch>
            <Route path="/login" component = {LogIn}/>
            <Route path="/signup" component = {SignUp}/>
            <Route path="/session" component = {Session}/>
            <Route path="/profile" component = {Profile}/>
            <Route path="/" component ={App} exact/>
        </Switch>
    </BrowserRouter>,
   document.getElementById('app'));