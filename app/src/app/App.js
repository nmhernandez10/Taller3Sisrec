import React, { Component } from 'react';
import Header from './components/Header';
import Footer from './components/Footer';

export default class App extends Component {

    state = {
        input: '',
        businesses: [],
        searching: true,
        top: false,
        link: null
    }

    handleInput = (e) => {
        const { value, id } = e.target;
        this.setState({
            [id]: value
        });
    }

    // getGeneralTop = () => {
    //     fetch('/api/user/409286/top').then(res => res.json()).then(data => {
    //         this.setState({
    //             businesses: data,
    //             top: true,
    //             searching: false
    //         });
    //     });
    // }

    componentDidMount() {
        document.dispatchEvent(new Event('component'));
        // this.getGeneralTop();
    }

    componentDidUpdate() {
        document.dispatchEvent(new Event('component'));
    }

    render() {

        return (
            <div>
                <div className="content">
                    <div className="name">
                        <div className="section black">
                            <br></br>
                            <div className="container">
                                <Header />
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



                <div className="divider"></div>
                <Footer />
            </div >
        )
    }
}
