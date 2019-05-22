import React, { Component } from 'react';
import { Redirect, Link } from 'react-router';

export default class App extends Component {

  state = {
    input: '',
    businesses: [],
    searching: true,
    top: true,
    link: null
  }

  linkTo = (path) => {
    this.setState({
      link: path
    });
  }

  stopSearching = () => {
    this.setState({
      businesses: [],
      input: '',
      searching: true
    }, this.getGeneralTop());
  }

  search = () => {
    event.preventDefault();
    if (this.state.input.replace(/\s/g, '').length == 0) {
      this.setState({
        businesses: [],
        searching: false,
        top: true
      });
    }
    else if (this.state.input !== '') {
      this.setState({
        searching: true
      }, () => {
        fetch('/api/business/byname/' + this.state.input).then(res => res.json()).then(data => {
          this.setState({
            businesses: data,
            searching: false,
            top: false
          });
        });
      });
    }
  }

  handleInput = (e) => {
    const { value, id } = e.target;
    this.setState({
      [id]: value
    });
  }

  getGeneralTop = () => {
    fetch('/api/user/409286/top').then(res => res.json()).then(data => {
      this.setState({
        businesses: data,
        top: true,
        searching: false
      });
    });
  }

  componentDidMount() {
    document.dispatchEvent(new Event('component'));
    this.getGeneralTop();
  }

  componentDidUpdate() {
    document.dispatchEvent(new Event('component'));
  }

  render() {

    if (JSON.parse(localStorage.getItem('loggeduser')) != null) {
      return <Redirect to='/session' />;
    } else if (this.state.link != null) {
      return <Redirect to={'/' + this.state.link} />;
    }

    const businessesCards = this.state.businesses.map((business, i) => {

      const images = business.Photos.map((photo, i) => {
        return (
          <li key={photo.id}>
            <img className="responsive-img" src={photo.route} />
          </li>
        );
      });

      return (
        <div key={business.id} className="col s6 l4 xl3">
          <div className="card medium hoverable">
            <div className="card-image">
              <div className="slider">
                <ul class="slides">
                  {images}
                </ul>
              </div>
            </div>
            <div className="card-content">
              <span className="card-title activator grey-text text-darken-4">{business.name}<i className="material-icons right">more_vert</i></span>
            </div>
            <div className="card-reveal">
              <span className="card-title grey-text text-darken-4">Attributes<i className="material-icons right">close</i></span>
              <p>{business.BusinessTags.map((tag, i) => {
                if (i == business.BusinessTags.length - 1) {
                  return (
                    tag.Tag.name
                  );
                }
                else {
                  return (
                    tag.Tag.name + " | "
                  );
                }
              })}</p>
            </div>
            <div className="card-action">
              {business.city + " - " + business.address}
            </div>
          </div>
        </div>
      );
    });

    return (
      <div className="content">

        <div className="main">

          <div className="section grey lighten-5">

            <br></br>

            <div className="container">

              <div className="row center">
                <div className="col s1">
                  <img className="responsive-img" src="./assets/colibri.png" />
                </div>
                <div className="col s2 offset-s7">
                  <a className="grey-text text-darken-2" onClick={() => this.linkTo("login")} href="#!">Log In</a>
                </div>
                <div className="col s2">
                  <a className="grey-text text-darken-2" onClick={() => this.linkTo("signup")} href="#!">Sign Up</a>
                </div>
              </div>

              <div className="row center">
                <div className="col s12">
                  <h2 className="grey-text text-darken-1">Welcome to Kweh!</h2>
                </div>
              </div>

              <div className="row center">
                <div className="col s12">
                  <h6 className="grey-text text-darken-1">Kwhere you can find the best businesses near you</h6>
                </div>
              </div>

              <div className="container row center">
                <div className="col s12">
                  <nav>
                    <div className="nav-wrapper grey lighten-1">
                      <form onSubmit={this.search}>
                        <div className="input-field">
                          <input id="input" type="search" onChange={this.handleInput} value={this.state.input} required />
                          <label className="label-icon" htmlFor="input"><i className="material-icons">search</i></label>
                          <i onClick={this.stopSearching} className="material-icons">close</i>
                        </div>
                      </form>
                    </div></nav>
                </div>
              </div>
            </div>

          </div>


          <div className="divider"></div>

          <div className="section">
            <div className="container row center">
              <div className="col s12">
                {
                  this.state.top ?
                    <h4 className="grey-text text-darken-3">Best businesses in Kweh</h4>
                    : <h4 className="grey-text text-darken-3">Search businesses result</h4>
                }
              </div>
            </div>
          </div>

          <div className="container section">
            <div className="row center">
              {
                this.state.searching ?
                  <div className="preloader-wrapper active">
                    <div className="spinner-layer spinner-red-only">
                      <div className="circle-clipper left">
                        <div className="circle"></div>
                      </div><div className="gap-patch">
                        <div className="circle"></div>
                      </div><div className="circle-clipper right">
                        <div className="circle"></div>
                      </div>
                    </div>
                  </div>
                  : this.state.businesses.length > 0 ?
                    businessesCards
                    : <h6>We did not find businesses related to your search</h6>
              }
            </div>
          </div>

        </div>


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
              <h6 className="grey-text text-darken-1">Made by</h6>
              <div className="col s2 offset-s4">
                <a className="grey-text text-darken-1" href="mailto:r.garcia11@uniandes.edu.co"><b>Rogelio García</b></a>
              </div>
              <div className="col s2">
                <a className="grey-text text-darken-1" href="mailto:nm.hernandez10@uniandes.edu.co"><b>Nicolás Hernández</b></a>
              </div>
            </div>

            <br></br>
            <div className="row center">
              <h6 className="grey-text text-darken-1">1717 Harrison St, San Francisco, CA 94103, USA</h6>
              <h6 className="grey-text text-darken-1">© 2019 Kweh Company Ltda.</h6>
            </div>
          </div>
          <div className="footer-copyright">
            <div className="container">
              <a className="grey-text text-lighten-1 right" href="#">Home</a>
            </div>
          </div>
        </footer>



      </div>
    )
  }
}
