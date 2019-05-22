import React, { Component } from 'react';
import { Redirect } from 'react-router';

export default class SignUp extends Component {

  state = {
    user_names: '',
    user_image: '',
    user_email: '',
    user_password: '',
    user_password_confirm: '',
    link: null
  }

  linkTo = (path) => {
    this.setState({
      link: path
    });
  }

  toLogIn = () => {
    this.props.toLogIn();
  }

  handleInput = (e) => {
    const { value, id } = e.target;
    this.setState({
      [id]: value
    });
  }

  handleSubmit = () => {

    console.log(this.state);
    if (this.state.user_password != this.state.user_password_confirm) {
      M.toast({ html: 'Passwords are not equal', classes: 'rounded' });
    }
    else if (this.state.user_password.length < 8) {
      M.toast({ html: 'Password must have minimum 8 tokens', classes: 'rounded' });
    }
    else if (this.state.user_password == '' || this.state.user_names == '' || this.state.user_image == '' || this.state.user_email == '') {
      M.toast({ html: 'Provide valid values for your account', classes: 'rounded' });
    }
    else {
      const nuevoUser = { names: this.state.user_names, image: this.state.user_image, email: this.state.user_email, password: this.state.user_password, yelp_id: this.state.user_email};

      fetch('/api/user', {
        method: 'POST',
        body: JSON.stringify(nuevoUser),
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }).then(res => {
        if (res.ok) {
          return res.json();
        }
        else {
          throw new Error("Another account already exists related to this e-mail");
        }
      }).then(data => {
        M.toast({ html: 'Your account has been created correctly', classes: 'rounded' });
        const idIdentified = data.id;
        localStorage.setItem('loggeduser', JSON.stringify({ id: idIdentified }));
        this.linkTo("session");
      }).catch(error => M.toast({ html: error.message, classes: 'rounded' }));
    }
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
                <a className="red-text text-darken-4"><i className="small material-icons">star</i></a>
              </div>
              <div className="col s2 offset-s9">
                <a className="grey-text text-darken-2" onClick={() => this.linkTo("")} href="#!">Home</a>
              </div>
            </div>
          </div>

          <div className="row center">
            <div className="col s12">
              <br></br>
              <h3 className="grey-text text-darken-3">Sign Up to Kweh!</h3>
              <h6 className="grey-text text-darken-3">or <a onClick={() => this.linkTo("login")} href="#">log in</a></h6>
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
                      <img className="responsive-img" src="https://images.pexels.com/photos/5049/forest-trees-fog-foggy.jpg?auto=compress&cs=tinysrgb&h=750&w=1260" />
                    </li>
                    <li>
                      <img className="responsive-img" src="https://images.pexels.com/photos/56944/pexels-photo-56944.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260" />
                    </li>
                    <li>
                      <img className="responsive-img" src="https://images.pexels.com/photos/589840/pexels-photo-589840.jpeg?auto=compress&cs=tinysrgb&h=750&w=1260" />
                    </li>
                  </ul>
                </div>
              </div>
            </div>


            <div className="col s4">

              <div className="row">
                <form className="col s12">
                  <div className="row">
                    <div className="input-field col s6">
                      <i className="material-icons prefix">person</i>
                      <input id="user_names" type="text" className="validate" onChange={this.handleInput} />
                      <label htmlFor="user_names">Names</label>
                    </div>
                    <div className="input-field col s6">
                      <i className="material-icons prefix">photo</i>
                      <input id="user_image" type="text" className="validate" onChange={this.handleInput} />
                      <label htmlFor="user_image">Photo</label>
                    </div>
                  </div>
                  <div className="row">
                    <div className="input-field col s12">
                      <i className="material-icons prefix">email</i>
                      <input id="user_email" type="email" className="validate" onChange={this.handleInput} />
                      <label htmlFor="user_email">E-mail</label>
                      <span className="helper-text" data-error="This e-mail is not valid" data-success="This e-mail is valid">Write your e-mail...</span>
                    </div>
                  </div>
                  <div className="row">
                    <div className="input-field col s6">
                      <i className="material-icons prefix">lock</i>
                      <input id="user_password" type="password" className="validate" onChange={this.handleInput} />
                      <label htmlFor="user_password">Password</label>
                      <span className="helper-text">Must have at least 8 tokens</span>
                    </div>
                    <div className="input-field col s6">
                      <i className="material-icons prefix">lock_outline</i>
                      <input id="user_password_confirm" type="password" className="validate" onChange={this.handleInput} />
                      <label htmlFor="user_password_confirm">Password confirmation</label>
                      <span className="helper-text">Rewrite your password</span>
                    </div>
                  </div>
                </form>

                <br></br>
                <br></br>

                <center><a onClick={this.handleSubmit} className="waves-effect waves-light btn grey lighten-5 grey-text text-darken-3">Sign Up</a></center>

              </div>

            </div>

          </div>

        </div>

        <br></br>

        <div className="divider"></div>

        <footer className="page-footer grey lighten-5">
          <div className="container">
            <div className="row center">
              <div className="col s2 offset-s1">
                <h6 className="grey-text text-darken-1">Features</h6>
              </div>
              <div className="col s2">
                <h6 className="grey-text text-darken-1">About</h6>
              </div>
              <div className="col s2">
                <h6 className="grey-text text-darken-1">Testimonials</h6>
              </div>
              <div className="col s2">
                <h6 className="grey-text text-darken-1">Contact</h6>
              </div>
              <div className="col s2">
                <h6 className="grey-text text-darken-1">Download</h6>
              </div>
            </div>

            <div className="divider"></div>

            <br></br>
            <div className="row center">
              <h6 className="grey-text text-darken-1">1717 Harrison St, San Francisco, CA 94103, USA</h6>
              <h6 className="grey-text text-darken-1">© 2019 Kweh Company Ltda.</h6>
            </div>
          </div>
          <div className="footer-copyright">
            <div className="container">
              <a className="grey-text text-lighten-1 right" onClick={() => this.linkTo('')} href="#">Home</a>
            </div>
          </div>
        </footer>



      </div >
    )
  }
}
