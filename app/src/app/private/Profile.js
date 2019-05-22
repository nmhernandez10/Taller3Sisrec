import React, { Component } from 'react';
import { Redirect } from 'react-router';
import dateFormat from 'dateformat';
import { Draggable, Droppable } from 'react-drag-and-drop'

export default class Profile extends Component {

    state = {
        input: '',
        user: {},
        dontliketags: [],
        dontliketagsids: [],
        liketags: [],
        liketagsids: [],
        searchedtags: [],
        logged: JSON.parse(localStorage.getItem('loggeduser')) == null ? false : true,
        link: null,
        searching: false,
        addinglike: false,
        addingdontlike: false,
        searched: false
    }

    linkTo = (path) => {
        this.setState({
            link: path
        });
    }

    stopSearching = () => {
        this.setState({
            searchedtags: [],
            input: '',
            searching: false,
            searched: false
        });
    }

    search = () => {
        event.preventDefault();
        if (this.state.input.replace(/\s/g, '').length == 0) {
            this.setState({
                searchedtags: [],
                searching: false,
                searched: false
            });
        }
        else if (this.state.input !== '') {
            this.setState({
                searching: true
            }, () => {
                fetch('/api/tag/byname/' + this.state.input).then(res => res.json()).then(data => {
                    let searchedtagslist = [];
                    for (let tag of data) {
                        if (this.state.liketagsids.filter(x => x == tag.id).length == 0 && this.state.dontliketagsids.filter(x => x == tag.id).length == 0) {
                            searchedtagslist.push(tag);
                        }
                    }
                    this.setState({
                        searchedtags: searchedtagslist,
                        searching: false,
                        searched: true
                    });
                });
            });
        }
    }

    logOut = () => {
        localStorage.setItem('loggeduser', JSON.stringify(null));
        this.setState({
            logged: false
        }, () => {
            M.toast({ html: 'Kweh will miss you', classes: 'rounded' });
        });
    }

    onDropLike = (added) => {
        let id = added.tag;
        let newtag = { like: true, TagId: id, UserId: this.state.user.id };

        this.setState({
            addinglike: true
        }, () => {
            fetch('/api/usertag', {
                method: 'POST',
                body: JSON.stringify(newtag),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            }).then(res => {
                if (res.ok) {
                    return res.json();
                }
                else {
                    console.log('Algún error ocurrió agregando');

                }
            }).then(data => {
                fetch('/api/tag/' + data.TagId).then(res => res.json()).then(tag => {
                    data.Tag = tag;
                    this.setState({
                        liketags: [...this.state.liketags, data],
                        liketagsids: [...this.state.liketagsids, data.TagId],
                        addinglike: false
                    }, () => this.dropFromSearched(data.TagId));
                });
            }).catch(error => console.log(error));
        });
    }

    onDropDontLike = (added) => {
        let id = added.tag;
        let newtag = { like: false, TagId: id, UserId: this.state.user.id };
        this.setState({
            addingdontlike: true
        }, () => {
            fetch('/api/usertag', {
                method: 'POST',
                body: JSON.stringify(newtag),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            }).then(res => {
                if (res.ok) {
                    return res.json();
                }
                else {
                    console.log('Algún error ocurrió agregando');

                }
            }).then(data => {
                fetch('/api/tag/' + data.TagId).then(res => res.json()).then(tag => {
                    data.Tag = tag;
                    this.setState({
                        dontliketags: [...this.state.dontliketags, data],
                        dontliketagsids: [...this.state.dontliketagsids, data.TagId],
                        addingdontlike: false
                    }, () => this.dropFromSearched(data.TagId));
                });
            }).catch(error => console.log(error));
        });
    }

    deleteLike = (usertag) => {
        fetch('/api/usertag/' + usertag.id, {
            method: 'DELETE'
        }).then(res => {
            if (res.ok) {
                return res.json();
            }
            else {
                console.log('Algún error ocurrió borrando');
            }
        }).then(data => {

            let modified = { content_updated: false };
            fetch('/api/user/' + this.state.user.id, {
                method: 'PUT',
                body: JSON.stringify(modified),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(data => {
                this.setState({
                    searchedtags: [...this.state.searchedtags, usertag.Tag]
                });
            }).catch(error => console.log(error));

        }).catch(error => console.log(error));
    }

    deleteDontLike = (usertag) => {
        fetch('/api/usertag/' + usertag.id, {
            method: 'DELETE'
        }).then(res => {
            if (res.ok) {
                return res.json();
            }
            else {
                console.log('Algún error ocurrió borrando');
            }
        }).then(data => {

            let modified = { content_updated: false };
            fetch('/api/user/' + this.state.user.id, {
                method: 'PUT',
                body: JSON.stringify(modified),
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(data => {
                this.setState({
                    searchedtags: [...this.state.searchedtags, usertag.Tag]
                });
            }).catch(error => console.log(error));

        }).catch(error => console.log(error));
    }

    dropFromSearched = (tagid) => {
        let newsearchedtags = [];
        for (let tag of this.state.searchedtags) {
            if (tag.id != tagid) {
                newsearchedtags.push(tag);
            }
        }

        let modified = { content_updated: false };
        fetch('/api/user/' + this.state.user.id, {
            method: 'PUT',
            body: JSON.stringify(modified),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            this.setState({
                searchedtags: newsearchedtags
            });
        }).catch(error => console.log(error));

    }

    handleInput = (e) => {
        const { value, id } = e.target;
        this.setState({
            [id]: value
        });
    }

    componentDidMount() {
        document.dispatchEvent(new Event('component'));
        var retrievedObject = JSON.parse(localStorage.getItem('loggeduser'));
        if (retrievedObject != null) {
            let idUser = retrievedObject.id;
            fetch('/api/user/forprofile/' + idUser).then(res => res.json()).then(data => {
                let liketagslist = [];
                let liketagsidslist = [];
                let dontliketagslist = [];
                let dontliketagsidslist = [];
                for (let usertag of data.UserTags) {
                    if (usertag.like) {
                        liketagslist.push(usertag);
                        liketagsidslist.push(usertag.TagId);
                    } else {
                        dontliketagslist.push(usertag);
                        dontliketagsidslist.push(usertag.TagId);
                    }
                }
                this.setState({
                    user: data,
                    liketags: liketagslist,
                    dontliketags: dontliketagslist,
                    liketagsids: liketagsidslist,
                    dontliketagsids: dontliketagsidslist
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

        const dontLikeTags = this.state.dontliketags.map((usertag, i) => {

            return (
                <div key={usertag.Tag.id} className="chip">
                    {usertag.Tag.name}
                    <i onClick={() => this.deleteDontLike(usertag)} className="close material-icons">close</i>
                </div>
            );

        });

        const likeTags = this.state.liketags.map((usertag, i) => {

            return (
                <div key={usertag.Tag.id} className="chip">
                    {usertag.Tag.name}
                    <i onClick={() => this.deleteLike(usertag)} className="close material-icons">close</i>
                </div>
            );

        });

        const searchedTags = this.state.searchedtags.map((tag, i) => {
            return (

                <div key={tag.id} className="chip">
                    <Draggable type="tag" data={tag.id}>
                        {tag.name}
                    </Draggable>
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
                                    <a className="grey-text text-darken-2" onClick={() => this.linkTo("session")} href="#!">Home</a>
                                </div>
                                <div className="col s2">
                                    <a className="grey-text text-darken-2 modal-trigger" href="#confirmModal">Log Out</a>
                                </div>
                            </div>

                            <div className="row center">
                                <div className="col s12">
                                    <h2 className="grey-text text-darken-1">This is your profile</h2>
                                </div>
                            </div>

                            <div className="row center">
                                <div className="col s12">
                                    <h6 className="grey-text text-darken-1">All the information you give to us is important</h6>
                                </div>
                            </div>

                        </div>

                    </div>

                    <div className="divider"></div>

                    <br></br>

                    {
                        this.state.user.names ?
                            <div className="section row">

                                <div className="col s4">
                                    <div className="container">
                                        <img className="responsive-img" src={this.state.user.image} />
                                        <h4>Personal information</h4>
                                        <table>
                                            <tbody>
                                                <tr>
                                                    <td><b>Names</b></td>
                                                    <td>{this.state.user.names}</td>
                                                </tr>
                                                <tr>
                                                    <td><b>E-mail</b></td>
                                                    <td>{this.state.user.email}</td>
                                                </tr>
                                                <tr>
                                                    <td><b>Signed Up Date</b></td>
                                                    <td>{dateFormat(this.state.user.createdAt, "dddd, mmmm dS, yyyy, h:MM:ss TT")}</td>
                                                </tr>
                                            </tbody>
                                        </table>

                                    </div>
                                </div>

                                <div className="col s7">
                                    <h4>What kind of businesses do you like?</h4>
                                    <h6>Search attributes that you would like businesses had. We will match this information to show you recommendations related to these tags. Once you looked for something, you can add it to any of both sides depending on your stand about it.</h6>
                                    <br></br>
                                    <div className="row center">
                                        <div className="col s4">
                                            <Droppable
                                                types={['tag']} // <= allowed drop types
                                                onDrop={this.onDropDontLike}>
                                                <div className="card-panel red darken-3">
                                                    <span className="white-text">Don't like</span>
                                                    <br></br>
                                                    <br></br>
                                                    {dontLikeTags}
                                                </div>
                                            </Droppable>
                                            {
                                                this.state.addingdontlike ?
                                                    <div className="progress red lighten-4">
                                                        <div className="indeterminate red darken-2"></div>
                                                    </div>
                                                    : null
                                            }

                                        </div>

                                        <div className="col s4">
                                            <nav>
                                                <div className="nav-wrapper grey lighten-1">
                                                    <form onSubmit={this.search}>
                                                        <div className="input-field">
                                                            <input id="input" type="search" onChange={this.handleInput} value={this.state.input} required />
                                                            <label className="label-icon" htmlFor="input"><i className="material-icons">search</i></label>
                                                            <i onClick={this.stopSearching} className="material-icons">close</i>
                                                        </div>
                                                    </form>
                                                    {

                                                        this.state.searching ?
                                                            <div>
                                                                <br></br>
                                                                <br></br>
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
                                                            </div>
                                                            : this.state.searchedtags.length > 0 && this.state.input == '' ?
                                                                <div>
                                                                    <br></br>
                                                                    <h6 className="grey-text text-darken-3">Recent attributes</h6>
                                                                    {searchedTags}
                                                                </div>
                                                                : this.state.searchedtags.length > 0 ?
                                                                    <div>
                                                                        <br></br>
                                                                        {searchedTags}
                                                                    </div>
                                                                    : this.state.input !== '' && this.state.searched ?
                                                                        <h6 className="grey-text text-darken-3">We did not find attributes related to your search</h6>
                                                                        : <h6 className="grey-text text-darken-3">Search attributes by name</h6>
                                                    }
                                                </div>
                                            </nav>
                                        </div>

                                        <div className="col s4">
                                            <Droppable
                                                types={['tag']} // <= allowed drop types
                                                onDrop={this.onDropLike}>
                                                <div className="card-panel green darken-1 large">
                                                    <span className="white-text">Do like</span>
                                                    <br></br>
                                                    <br></br>
                                                    {likeTags}
                                                </div>
                                            </Droppable>
                                            {
                                                this.state.addinglike ?
                                                    <div className="progress green lighten-4">
                                                        <div className="indeterminate green darken-2"></div>
                                                    </div>
                                                    : null
                                            }

                                        </div>
                                    </div>
                                </div>

                            </div>
                            : <div className="section row center">
                                <div className="col s12">
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
                            </div>
                    }




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