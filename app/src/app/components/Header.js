import React from 'react';

const header = () => {
    return (
        <div className="row center">
            <div className="col s1">
                <img src="./assets/colibri.png" alt="colibri" className="responsive-img" />
            </div>
            <div className="col s2 offset-s7">
                <a href="#!" className="grey-text text-darken-2">Log in</a>
            </div>
            <div className="col s2">
                <a href="#!" className="grey-text text-darken-2">Sign up</a>
            </div>
        </div>
);
};

export default header;