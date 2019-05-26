import React from 'react';

const footer = () => {
    return (<footer className="page-footer grey lighten-5">
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
    </footer>);
};

export default footer;