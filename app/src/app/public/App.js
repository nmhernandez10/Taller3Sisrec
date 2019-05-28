import React, { Component } from 'react';
import { Redirect, Link } from 'react-router';
import Footer from '../components/Footer';
export default class App extends Component {

    state = {
        input: '',
        movies: [],
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
            movies: [],
            input: '',
            searching: true
        }, this.getGeneralTop());
    }

    search = () => {
        event.preventDefault();
        if (this.state.input.replace(/\s/g, '').length == 0) {
            this.setState({
                movies: [],
                searching: false,
                top: true
            });
        }
        else if (this.state.input !== '') {
            this.setState({
                searching: true
            }, () => {
                fetch('/api/movie/byname/' + this.state.input).then(res => res.json()).then(data => {
                    this.setState({
                        movies: data,
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
        fetch('/api/user/1/top').then(res => res.json()).then(data => {
            this.setState({
                movies: data,
                top: true,
                searching: false
            });
        });
    }

    componentDidMount() {
        document.dispatchEvent(new Event('component'));
        //this.getGeneralTop();
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

        const moviesCards = this.state.movies.map((movie, i) => {

            return (
                <div key={movie.id} className="col s6 l4 xl3">
                    <div className="card small hoverable">
                        <div className="card-image">
                            <img className="responsive-img" src={movie.photo} />
                        </div>
                        <div className="card-content">
                            <span className="card-title activator grey-text text-darken-4 truncate">{movie.name}<i className="material-icons right">more_vert</i></span>
                        </div>
                        <div className="card-reveal">
                            <span className="card-title grey-text text-darken-4">Attributes<i className="material-icons right">close</i></span>
                            <p><b>Title: </b>{movie.name}</p>
                            <p>{movie.MovieTags.map((tag, i) => {
                                if (i == movie.MovieTags.length - 1) {
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
                            {movie.year}
                        </div>
                    </div>
                </div>
            );
        });

        return (
            <div className="content">

                <div className="main">

                    <div className="section grey darken-4">

                        <br></br>

                        <div className="container">

                            <div className="row center">
                                <div className="col s1">
                                    <i className="yellow-text text-darken-2 medium material-icons">camera</i>
                                </div>
                                <div className="col s2 offset-s7">
                                    <a className="white-text" onClick={() => this.linkTo("login")} href="#!">Log In</a>
                                </div>
                                <div className="col s2">
                                    <a className="white-text" onClick={() => this.linkTo("signup")} href="#!">Sign Up</a>
                                </div>
                            </div>

                            <div className="row center">
                                <div className="col s12">
                                    <h2 className="white-text">Welcome to Shutter!</h2>
                                </div>
                            </div>

                            <div className="row center">
                                <div className="col s12">
                                    <h6 className="white-text">Where you can find the best movies for you</h6>
                                </div>
                            </div>

                            <div className="container row center">
                                <div className="col s12">
                                    <nav>
                                        <div className="nav-wrapper grey darken-3">
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

                    <div className="grey ligthen-2 divider"></div>

                    <div className="section">
                        <div className="container row center">
                            <div className="col s12">
                                {
                                    this.state.top ?
                                        <h4 className="grey-text text-darken-3">Best movies in Shutter</h4>
                                        : <h4 className="grey-text text-darken-3">Search movies result</h4>
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
                                    : this.state.movies.length > 0 ?
                                        moviesCards
                                        : <h6>We did not find movies related to your search</h6>
                            }
                        </div>
                    </div>

                </div>
                <div className="grey ligthen-2 divider"></div>
                <Footer />
            </div >
        )
    }
}
