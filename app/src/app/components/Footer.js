import React from 'react';

const footer = () => {
    return (<footer className="page-footer grey darken-4">
        <div className="container">

            <br></br>
            <div className="row center">
                <h6 className="white-text">Made by</h6>
                <div className="col s2 offset-s3">
                    <a className="white-text" href="mailto:r.garcia11@uniandes.edu.co"><b>Rogelio García</b></a>
                </div>
                <div className="col s2">
                    <a className="white-text" href="mailto:nm.hernandez10@uniandes.edu.co"><b>Nicolás Hernández</b></a>
                </div>
                <div className="col s2">
                    <a className="white-text" href="mailto:nm.hernandez10@uniandes.edu.co"><b>Tatiana Rincón</b></a>
                </div>
            </div>

            <br></br>
            <div className="row center">
                <h6 className="white-text">1717 Harrison St, San Francisco, CA 94103, USA</h6>
                <h6 className="white-text">© 2019 Shutter Company Ltda.</h6>
            </div>
        </div>
        <div className="footer-copyright">
            <div className="container">
                <a className="white-text right" href="#">Home</a>
            </div>
        </div>
    </footer>);
};

export default footer;