import React, { Component } from 'react';
import { Redirect } from 'react-router';
import StarRatings from 'react-star-ratings';

export default class Session extends Component {

    state = {
        input: '',
        user: {},
        logged: JSON.parse(localStorage.getItem('loggeduser')) == null ? false : true,
        link: null,
        tags: [],
        results: [],
        recommendations: [],
        recommended: false,
        historicreviews: [],
        searching: true,
        searched: false,
        reviews: {},
        svd_updated: true,
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
                M.toast({ html: 'Provide a name or some attributes to search businesses', classes: 'rounded' });
            }
            else {
                this.setState({
                    searching: true
                }, () => {
                    fetch('/api/business/byname/' + this.state.input).then(res => res.json()).then(data => {
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
                fetch('/api/business/byattributes/name', {
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
        let ratingbody = { BusinessId: parseInt(name), UserId: this.state.user.id, stars: newRating, date: Date.now(), svd_updated: false };
        fetch('/api/review', {
            method: 'PUT',
            body: JSON.stringify(ratingbody),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            let reviews = this.state.reviews;
            reviews[data.BusinessId] = data.stars;
            this.setState({
                reviews: reviews,
                svd_updated: false
            }, () => this.addToHistoricReviews(data));
        });
    }

    addToHistoricReviews = (reviewdata) => {
        let alreadyin = false;
        for (let historicreview of this.state.historicreviews) {
            if (reviewdata.BusinessId == historicreview.BusinessId) {
                alreadyin = true;
                break;
            }
        }
        if (!alreadyin) {
            fetch('/api/business/' + reviewdata.BusinessId).then(res => res.json()).then(data => {
                reviewdata.Business = data;
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
            fetch('/api/user/' + this.state.user.id + '/top').then(res => res.json()).then(data => {

                if (data.length == 0) {
                    this.getGeneralTop();
                }

                this.setState({
                    recommendations: data,
                    searching: false,
                    recommended: true
                });
            });
        });

    }

    getGeneralTop = () => {
        fetch('/api/user/409286/top').then(res => res.json()).then(data => {
            this.setState({
                generaltop: data
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
                let updated = true;
                let reviews = {};
                for (let review of data.Reviews) {
                    reviews[review.BusinessId] = review.stars;
                    if (!review.svd_updated) {
                        updated = false;
                    }
                }
                this.setState({
                    user: data,
                    reviews: reviews,
                    svd_updated: updated,
                    historicreviews: data.Reviews
                }, () => {
                    this.getRecommendations();
                });
            }).catch(error => { this.setState({ logged: false }); });
        }
    }

    componentDidUpdate() {
        document.dispatchEvent(new Event('component'));
    }

    render() {

        if (!this.state.logged) {
            return <Redirect to='/' />;
        } else if (this.state.link != null) {
            return <Redirect to={'/' + this.state.link} />;
        }

        const topdivider = 4;
        let svd = false;
        let cb = false;

        const generaltopCards = this.state.generaltop.map((business, i) => {

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
                                <ul className="slides">
                                    {images}
                                </ul>
                            </div>
                        </div>
                        <div className="card-content">
                            <span className="card-title activator grey-text text-darken-4">{business.name}<i className="material-icons right">more_vert</i></span>
                            <br></br>
                            {business.city + " - " + business.address}
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
                            <StarRatings
                                rating={this.state.reviews[business.id] || 0}
                                starRatedColor='rgb(255, 206, 51)'
                                changeRating={this.changeRating}
                                numberOfStars={5}
                                name={String(business.id)}
                                starDimension="25px"
                            />
                        </div>
                    </div>
                </div>
            );
        });

        const reviewsCards = this.state.historicreviews.map((review, i) => {

            const business = review.Business;

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
                                <ul className="slides">
                                    {images}
                                </ul>
                            </div>
                        </div>
                        <div className="card-content">
                            <span className="card-title activator grey-text text-darken-4">{business.name}<i className="material-icons right">more_vert</i></span>
                            <br></br>
                            {business.city + " - " + business.address}
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
                            <StarRatings
                                rating={this.state.reviews[business.id] || 0}
                                starRatedColor='rgb(255, 206, 51)'
                                changeRating={this.changeRating}
                                numberOfStars={5}
                                name={String(business.id)}
                                starDimension="25px"
                            />
                        </div>
                    </div>
                </div>
            );
        });

        const businessesCards = this.state.results.map((business, i) => {

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
                                <ul className="slides">
                                    {images}
                                </ul>
                            </div>
                        </div>
                        <div className="card-content">
                            <span className="card-title activator grey-text text-darken-4">{business.name}<i className="material-icons right">more_vert</i></span>
                            <br></br>
                            {business.city + " - " + business.address}
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
                            <StarRatings
                                rating={this.state.reviews[business.id] || 0}
                                starRatedColor='rgb(255, 206, 51)'
                                changeRating={this.changeRating}
                                numberOfStars={5}
                                name={String(business.id)}
                                starDimension="25px"
                            />
                        </div>
                    </div>
                </div>
            );
        });

        const recommendationsSVDCards = this.state.recommendations.map((business, i) => {

            if ((this.state.recommendations.length <= topdivider && this.state.user.top.substring(0, 1) == ',') || (this.state.recommendations.length > topdivider && i >= topdivider)) {

                svd = true;

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
                                    <ul className="slides">
                                        {images}
                                    </ul>
                                </div>
                            </div>
                            <div className="card-content">
                                <span className="card-title activator grey-text text-darken-4">{business.name}<i className="material-icons right">more_vert</i></span>
                                <br></br>
                                {business.city + " - " + business.address}
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
                                <StarRatings
                                    rating={this.state.reviews[business.id] || 0}
                                    starRatedColor='rgb(255, 206, 51)'
                                    changeRating={this.changeRating}
                                    numberOfStars={5}
                                    name={String(business.id)}
                                    starDimension="25px"
                                />
                            </div>
                        </div>
                    </div>
                );
            }
        });

        const recommendationsCBCards = this.state.recommendations.map((business, i) => {

            if ((this.state.recommendations.length <= topdivider && this.state.user.top.substring(0, 1) != ',') || (this.state.recommendations.length > topdivider && i < topdivider)) {

                cb = true;
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
                                    <ul className="slides">
                                        {images}
                                    </ul>
                                </div>
                            </div>
                            <div className="card-content">
                                <span className="card-title activator grey-text text-darken-4">{business.name}<i className="material-icons right">more_vert</i></span>
                                <br></br>
                                {business.city + " - " + business.address}
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
                                <StarRatings
                                    rating={this.state.reviews[business.id] || 0}
                                    starRatedColor='rgb(255, 206, 51)'
                                    changeRating={this.changeRating}
                                    numberOfStars={5}
                                    name={String(business.id)}
                                    starDimension="25px"
                                />
                            </div>
                        </div>
                    </div>
                );
            }
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
                                    <a className="grey-text text-darken-2" onClick={() => this.linkTo("profile")} href="#!">Profile</a>
                                </div>
                                <div className="col s2">
                                    <a className="grey-text text-darken-2 modal-trigger" href="#confirmModal">Log Out</a>
                                </div>
                            </div>

                            <div className="row center">
                                <div className="col s12">
                                    <h2 className="grey-text text-darken-1">Hello, {this.state.user.names}!</h2>
                                </div>
                            </div>

                            <div className="row center">
                                <div className="col s12">
                                    <h6 className="grey-text text-darken-1">Let us help you discover the business for you</h6>
                                </div>
                            </div>

                            <div className="section container">
                                <div className="row">
                                    <div className="container input-field col s12">
                                        <input placeholder="By name" id="input" type="text" onChange={this.handleInput} value={this.state.input} />
                                    </div>
                                </div>
                                <div className="row">
                                    <div className="container input-field col s12">
                                        <div className="chips chips-autocomplete">
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
                                        {businessesCards}
                                    </div>
                                    : this.state.searched ?
                                        <div className="center">
                                            <h4>Search results</h4>
                                            <h5>No businesses were found according to your search inputs</h5>
                                        </div>
                                        : null
                        }
                    </div>

                    <div className="section row container">
                        {
                            this.state.searching ?
                                null
                                : this.state.recommendations.length > 0 ?
                                    <div className="center">
                                        <h4>Our recommendations for you</h4>
                                        {
                                            (!this.state.svd_updated || !this.state.user.content_updated) && !(recommendationsSVDCards.length > 0 && svd) && !(recommendationsCBCards.length > 0 && cb) ?
                                                <div>
                                                    <h6>We are making new recommendations...</h6>
                                                    <br></br>
                                                    <h5>This recommendations are a general set of best ranked businesses</h5>
                                                    <br></br>
                                                    {generaltopCards}
                                                </div>
                                                : !this.state.svd_updated && !(recommendationsSVDCards.length > 0 && svd) ?
                                                    <div>
                                                        <h6>We are making new recommendations based on your ratings and people who are similar to you...</h6>
                                                        <br></br>
                                                    </div>
                                                    : !this.state.user.content_updated && !(recommendationsCBCards.length > 0 && cb) ?
                                                        <div>
                                                            <h6>We are making new recommendations based on the business attributes you like and don't like...</h6>
                                                            <br></br>
                                                        </div>
                                                        : null
                                        }
                                        {
                                            recommendationsSVDCards.length > 0 && svd ?
                                                <div className="row section">
                                                    <h5>This recommendations are based on your ratings and people who are similar to you</h5>
                                                    {
                                                        !this.state.svd_updated ?
                                                            <div>
                                                                <h6>We are making new of these recommendations...</h6>
                                                            </div>
                                                            : null
                                                    }
                                                    <br></br>
                                                    {recommendationsSVDCards}
                                                </div>
                                                : null
                                        }
                                        {
                                            recommendationsCBCards.length > 0 && cb ?
                                                <div className="row section">
                                                    <h5>These recommendations are based on the business attributes you like and don't like</h5>

                                                    {
                                                        !this.state.user.content_updated ?
                                                            <div>
                                                                <h6>We are making new of these recommendations...</h6>
                                                            </div>
                                                            : null
                                                    }
                                                    <br></br>
                                                    {recommendationsCBCards}
                                                </div>
                                                : null
                                        }
                                    </div>
                                    : this.state.recommended ?
                                        <div className="center">
                                            <h4>Our recommendations for you</h4>
                                            {
                                                !this.state.svd_updated || !this.state.user.content_updated ?
                                                    <div>
                                                        <h6>We are making new recommendations...</h6>
                                                        <br></br>
                                                    </div>
                                                    :
                                                    <div>
                                                        <h6>We need more information about you to build customized recommendations</h6>
                                                        <br></br>
                                                    </div>
                                            }
                                            <h5>These recommendations are a general set of best ranked businesses</h5>
                                            <br></br>
                                            {generaltopCards}
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
                                        <h6>Please, rate some businesses</h6>
                                    </div>
                        }
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
