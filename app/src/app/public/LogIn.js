import React, { Component } from 'react';
import { Redirect } from 'react-router';
import Footer from '../components/Footer';


export default class LogIn extends Component {

  state = {
    user_email: '',
    user_password: '',
    link: null
  }

  linkTo = (path) => {
    this.setState({
      link: path
    });
  }

  toSignUp = () => {
    this.props.toSignUp();
  }

  handleInput = (e) => {
    const { value, id } = e.target;
    this.setState({
      [id]: value
    });
  }

  handleSubmit = () => {
    if (this.state.user_password == '' || this.state.user_email == '') {
      M.toast({ html: 'Provide valid values of your account', classes: 'rounded' });
    }
    fetch('/api/user/byemail/' + this.state.user_email).then(res => res.json()).then(data => {
      if (data.length > 0) {
        M.toast({ html: 'Welcome to Kweh', classes: 'rounded' });
        localStorage.setItem('loggeduser', JSON.stringify({ id: data[0].id }));
        this.linkTo("session");
      }
      else {
        M.toast({ html: 'Information does not match with any account', classes: 'rounded' });
      }
    });
  }

  componentDidMount() {
    document.dispatchEvent(new Event('componentbigger'));
  }

  render() {

    if (JSON.parse(localStorage.getItem('loggeduser')) != null) {
      return <Redirect to='/session' />;
    } else if (this.state.link != null) {
      return <Redirect to={'/' + this.state.link} />;
    }

    return (
      <div className="content">

        <div className="main section">

          <br></br>

          <div className="container">
            <div className="row center">
              <div className="col s1">
                <i className="yellow-text text-darken-2 medium material-icons">camera</i>
              </div>
              <div className="col s2 offset-s9">
                <a className="grey-text text-darken-2" onClick={() => this.linkTo("")} href="#!">Home</a>
              </div>
            </div>
          </div>

          <div className="row center">
            <div className="col s12">
              <br></br>
              <h3 className="grey-text text-darken-3">Log In to Shutter!</h3>
              <h6 className="grey-text text-darken-3">or <a onClick={() => this.linkTo("signup")} href="#">sign your account up</a></h6>
              <br></br>
              <br></br>
            </div>
          </div>

          <div className="row">


            <div className="col s6">
              <div className="container">
                <div className="slider hoverable">
                  <ul className="slides">
                    <li>
                      <img className="responsive-img" src="https://images.pexels.com/photos/1624237/pexels-photo-1624237.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260" />
                    </li>
                    <li>
                      <img className="responsive-img" src="https://images.pexels.com/photos/2118174/pexels-photo-2118174.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260" />
                    </li>
                    <li>
                      <img className="responsive-img" src="https://images.pexels.com/photos/917494/pexels-photo-917494.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260" />
                    </li>
                  </ul>
                </div>
              </div>
            </div>


            <div className="col s4">

              <div className="row">
                <form className="col s12">

                  <br></br>
                  <div className="section row">
                    <div className="input-field col s12">
                      <i className="material-icons prefix">email</i>
                      <input id="user_email" type="email" className="validate" onChange={this.handleInput} />
                      <label htmlFor="user_email">E-mail</label>
                      <span className="helper-text" data-error="This e-mail is not valid" data-success="This e-mail is valid">Write your e-mail...</span>
                    </div>
                  </div>
                  <div className="section row">
                    <div className="input-field col s12">
                      <i className="material-icons prefix">lock</i>
                      <input id="user_password" type="password" className="validate" onChange={this.handleInput} />
                      <label htmlFor="user_password">Password</label>
                    </div>
                  </div>

                </form>

                <br></br>
                <br></br>

                <center>
                  <a onClick={this.handleSubmit} className="waves-effect waves-light btn yellow darken-2 white-text">Log In</a>
                </center>
                {/**<a onClick = {this.toSignUp} href="#">Did you forget your password?</a>*/}

              </div>

            </div>

          </div>

        </div>

        <br></br>

        <div className="divider"></div>

        <Footer />
      </div>
    )
  }
}
