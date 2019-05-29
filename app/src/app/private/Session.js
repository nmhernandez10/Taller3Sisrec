import React, { Component } from 'react';
import { Redirect } from 'react-router';
import StarRatings from 'react-star-ratings';
import Footer from '../components/Footer';

export default class Session extends Component {

    state = {
        input: '',
        user: {},
        logged: JSON.parse(localStorage.getItem('loggeduser')) == null ? false : true,
        link: null,
        tags: [],
        results: [],
        recommendationonto: [],
        recommendationsvd: [],
        recommended: false,
        historicreviews: [],
        searching: true,
        searched: false,
        reviews: {},
        generaltop: []
    }

    linkTo = (path) => {
        this.setState({
            link: path
        });
    }

    logOut = () => {
        localStorage.setItem('loggeduser', JSON.stringify(null));
        this.setState({
            logged: false
        }, () => {
            M.toast({ html: 'Kweh will miss you', classes: 'rounded' });
        });
    }

    handleInput = (e) => {
        const { value, id } = e.target;
        this.setState({
            [id]: value
        });
    }

    createCard = (movie) => {
        return (
            <div key={movie.id} className="col s6 l4 xl3">
                <div className="card medium hoverable">
                    <div className="card-image">
                        <img className="responsive-img" src={movie.photo} />
                    </div>
                    <div className="card-content">
                        <span className="card-title activator grey-text text-darken-4 truncate col s11">{movie.name}</span>
                        <br></br>
                        {movie.director + " - " + movie.year}
                    </div>
                    <div className="card-reveal">
                        <span className="card-title grey-text text-darken-4">Attributes<i className="material-icons right">close</i></span>
                        <p><b>Title: </b>{movie.name}</p>
                        <p><b>Director: </b>{movie.director}</p>
                        <p><b>Actors: </b>{movie.actors.replace(/,/g, ", ")}</p>
                        <p><b>Tags</b></p>
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
                        <StarRatings
                            rating={this.state.reviews[movie.id] || 0}
                            starRatedColor='rgb(255, 206, 51)'
                            changeRating={this.changeRating}
                            numberOfStars={5}
                            name={String(movie.id)}
                            starDimension="25px"
                        />
                    </div>
                </div>
            </div>);
    }

    initializeAutocomplete = () => {
        fetch('/api/tagnames').then(res => res.json()).then(data => {
            let tagnames = {};
            for (let tag of data) {
                tagnames[tag.name] = null;
            }
            let elems = document.querySelectorAll('.chips');
            M.Chips.init(elems, {
                placeholder: "By attributes", autocompleteOptions: {
                    data: tagnames, limit: 5,
                    minLength: 1
                },
                onChipAdd: this.onTagAdded,
                onChipDelete: this.onTagDeleted,
                secondaryPlaceholder: "More attributes"
            });
        });
    }

    onTagDeleted = (e, data) => {
        let newtags = [];
        let tagname = data.textContent.substring(0, data.textContent.length - 5);
        for (let tag of this.state.tags) {
            if (tag != tagname) {
                newtags.push(tag);
            }
        }
        this.setState({
            tags: newtags
        });
    }

    onTagAdded = (e, data) => {
        let tagname = data.textContent.substring(0, data.textContent.length - 5);
        this.setState({
            tags: [...this.state.tags, tagname]
        });
    }

    stopSearch = () => {
        this.setState({
            searched: false,
            searching: false,
            results: [],
            resultsratings: [],
            input: ''
        });
    }

    search = () => {
        if (this.state.tags.length == 0) {
            if (this.state.input.replace(/\s/g, '').length == 0) {
                this.stopSearch();
                M.toast({ html: 'Provide a name or some attributes to search movies', classes: 'rounded' });
            }
            else {
                this.setState({
                    searching: true
                }, () => {
                    fetch('/api/movie/byname/' + this.state.input).then(res => res.json()).then(data => {
                        this.setState({
                            results: data,
                            searched: true,
                            searching: false
                        });
                    });
                });
            }
        }
        else {
            let getBody = { attributes: this.state.tags, name: this.state.input };

            if (this.state.input.replace(/\s/g, '').length == 0) {
                getBody = { attributes: this.state.tags, name: '' };
            }

            this.setState({
                searching: true
            }, () => {
                fetch('/api/movie/byattributes/name', {
                    method: 'PUT',
                    body: JSON.stringify(getBody),
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }
                }).then(res => res.json()).then(data => {
                    this.setState({
                        results: data,
                        searched: true,
                        searching: false
                    });
                });
            });
        }
    }

    changeRating = (newRating, name) => {
        let ratingbody = { MovieId: parseInt(name), UserId: this.state.user.id, stars: newRating, date: Date.now(), svd_updated: false };
        fetch('/api/review', {
            method: 'PUT',
            body: JSON.stringify(ratingbody),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            let reviews = this.state.reviews;
            reviews[data.MovieId] = data.stars;
            this.setState({
                reviews: reviews,
                svd_updated: false
            }, () => this.addToHistoricReviews(data));
        });
    }

    addToHistoricReviews = (reviewdata) => {
        let alreadyin = false;
        for (let historicreview of this.state.historicreviews) {
            if (reviewdata.MovieId == historicreview.MovieId) {
                alreadyin = true;
                break;
            }
        }
        if (!alreadyin) {
            fetch('/api/movie/' + reviewdata.MovieId).then(res => res.json()).then(data => {
                reviewdata.Movie = data;
                this.setState({
                    historicreviews: [...this.state.historicreviews, reviewdata]
                });
            });
        }
    }

    getRecommendations = () => {

        this.setState({
            searching: true
        }, () => {
            fetch('/api/user/' + this.state.user.id + '/toponto').then(res => res.json()).then(dataonto => {

                this.setState({
                    recommendationonto: dataonto
                }, () => {
                    fetch('/api/user/' + this.state.user.id + '/topsvd').then(res => res.json()).then(datasvd => {

                        this.setState({
                            recommendationsvd: datasvd,
                            searching: false,
                            recommended: true
                        }, () => this.getGeneralTop());
                    });
                });
            });
        });
    }

    getGeneralTop = () => {
        fetch('/api/user/283230/toponto').then(res => res.json()).then(data => {
            this.setState({
                generaltop: data
            }, () => {
                var elems = document.querySelectorAll('.slider');
                M.Slider.init(elems, { indicators: false, interval: 5000, height: window.innerHeight * 0.6 });
            });
        });
    }

    componentDidMount() {
        document.dispatchEvent(new Event('component'));

        this.initializeAutocomplete();

        var retrievedObject = JSON.parse(localStorage.getItem('loggeduser'));
        if (retrievedObject != null) {
            let idUser = retrievedObject.id;
            fetch('/api/user/' + idUser).then(res => res.json()).then(data => {
                let reviews = {};
                for (let review of data.Reviews) {
                    reviews[review.MovieId] = review.stars;
                }
                this.setState({
                    user: data,
                    reviews: reviews,
                    historicreviews: data.Reviews
                }, () => {
                    this.getRecommendations();
                });
            }).catch(error => { this.setState({ logged: false }); });
        }
    }

    render() {

        if (!this.state.logged) {
            return <Redirect to='/' />;
        } else if (this.state.link != null) {
            return <Redirect to={'/' + this.state.link} />;
        }

        const generalTopSlides = this.state.generaltop.map((movie, i) => {
            return (
                <li key={movie.id}>
                    <img src={movie.photo} />
                    <div className="caption center-align">
                        <h3>{movie.name}</h3>
                        <h5 className="light grey-text text-lighten-3">{movie.director} - {movie.year}</h5>
                    </div>
                </li>
            );
        });

        const generaltopCards = this.state.generaltop.map((movie, i) => {
            return (
                this.createCard(movie)
            );
        });

        const reviewsCards = this.state.historicreviews.map((review, i) => {

            const movie = review.Movie;

            return (
                this.createCard(movie)
            );
        });

        const moviesCards = this.state.results.map((movie, i) => {

            return (
                this.createCard(movie)
            );
        });

        const recommendationsSVDCards = this.state.recommendationsvd.map((movie, i) => {

            return (
                this.createCard(movie)
            );

        });

        const recommendationsOntoCards = this.state.recommendationonto.map((movie, i) => {

            return (
                this.createCard(movie)
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
                                    <a className="white-text" onClick={() => this.linkTo("profile")} href="#!">Profile</a>
                                </div>
                                <div className="col s2">
                                    <a className="white-text modal-trigger" href="#confirmModal">Log Out</a>
                                </div>
                            </div>

                            <div className="row center">
                                <div className="col s12">
                                    <h2 className="white-text">Hello, {this.state.user.names}!</h2>
                                </div>
                            </div>

                            <div className="row center">
                                <div className="col s12">
                                    <h6 className="white-text">Let us help you discover the movie for you</h6>
                                </div>
                            </div>

                            <div className="section container">
                                <div className="row">
                                    <div className="container input-field col s12">
                                        <input className="white-text" placeholder="By name" id="input" type="text" onChange={this.handleInput} value={this.state.input} />
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="container input-field col s12">
                                        <div className="chips">
                                            <input className="white-text" />
                                        </div>
                                    </div>
                                </div>
                                <center>
                                    <a onClick={this.stopSearch} className="waves-effect waves-light btn grey darken-3">Cancel</a>{" "}<a onClick={this.search} className="waves-effect waves-light btn grey lighten-2 grey-text text-darken-3">Search</a>
                                </center>
                            </div>

                        </div>

                    </div>

                    <div className="divider"></div>

                    <div className="section row container">

                        <br></br>
                        <h4 className="center">Best ranked movies</h4>
                        <br></br>

                        <div className="slider">
                            <ul className="slides">
                                {generalTopSlides}
                            </ul>
                        </div>

                        {
                            this.state.searching ?
                                <div className="col s12 center">
                                    <br></br>
                                    <div className="preloader-wrapper big active">
                                        <div className="spinner-layer spinner-blue">
                                            <div className="circle-clipper left">
                                                <div className="circle"></div>
                                            </div><div className="gap-patch">
                                                <div className="circle"></div>
                                            </div><div className="circle-clipper right">
                                                <div className="circle"></div>
                                            </div>
                                        </div>

                                        <div className="spinner-layer spinner-red">
                                            <div className="circle-clipper left">
                                                <div className="circle"></div>
                                            </div><div className="gap-patch">
                                                <div className="circle"></div>
                                            </div><div className="circle-clipper right">
                                                <div className="circle"></div>
                                            </div>
                                        </div>

                                        <div className="spinner-layer spinner-yellow">
                                            <div className="circle-clipper left">
                                                <div className="circle"></div>
                                            </div><div className="gap-patch">
                                                <div className="circle"></div>
                                            </div><div className="circle-clipper right">
                                                <div className="circle"></div>
                                            </div>
                                        </div>

                                        <div className="spinner-layer spinner-green">
                                            <div className="circle-clipper left">
                                                <div className="circle"></div>
                                            </div><div className="gap-patch">
                                                <div className="circle"></div>
                                            </div><div className="circle-clipper right">
                                                <div className="circle"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                : this.state.results.length > 0 && this.state.searched ?
                                    <div className="center">
                                        <h4>Search results</h4>
                                        <br></br>
                                        {moviesCards}
                                    </div>
                                    : this.state.searched ?
                                        <div className="center">
                                            <h4>Search results</h4>
                                            <h5>No movies were found according to your search inputs</h5>
                                        </div>
                                        : null
                        }
                    </div>

                    <div className="section row container">
                        {
                            this.state.searching ?
                                null
                                : this.state.recommendationsvd.length > 0 || this.state.recommendationonto.length > 0 ?
                                    <div className="center">
                                        <h4>Our recommendations for you</h4>
                                        {
                                            this.state.recommendationsvd.length > 0 ?
                                                <div className="row section">
                                                    <h5>These recommendations are based on your ratings and people who are similar to you</h5>
                                                    <br></br>
                                                    {recommendationsSVDCards}
                                                </div>
                                                : null
                                        }
                                        {
                                            this.state.recommendationonto.length > 0 ?
                                                <div className="row section">
                                                    <h5>These recommendations are based on the movie attributes you like and don't like</h5>
                                                    <br></br>
                                                    {recommendationsOntoCards}
                                                </div>
                                                : null
                                        }
                                    </div>
                                    : this.state.recommended ?
                                        <div className="center">
                                            <h4>Our recommendations for you</h4>
                                            <h6>We need more information about you to build customized recommendations</h6>
                                        </div>
                                        : null
                        }
                    </div>

                    <div className="section row container">
                        {
                            this.state.searching ?
                                null
                                : this.state.user.Reviews.length > 0 ?
                                    <div className="center">
                                        <h4>All your reviews</h4>
                                        <br></br>
                                        {reviewsCards}
                                    </div>
                                    : <div className="center">
                                        <h4>All your reviews</h4>
                                        <h6>Please, rate some movies</h6>
                                    </div>
                        }
                    </div>

                </div>

                <br></br>

                <div className="divider"></div>

                <Footer />

                {/* Modals */}

                <div id="confirmModal" className="modal">
                    <div className="modal-content">
                        <h4>Log Out</h4>
                        <p>Are you sure you want to log out?</p>
                    </div>
                    <div className="modal-footer">
                        <a href="#" className="modal-close waves-effect waves-green btn-flat">No</a>
                        <a onClick={this.logOut} className="modal-close waves-effect waves-green btn-flat">Sí</a>
                    </div>
                </div>

            </div>
        )
    }
}
