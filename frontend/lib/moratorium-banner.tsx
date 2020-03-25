import React, { useState } from 'react'
import { SimpleProgressiveEnhancement } from './progressive-enhancement';
import classnames from 'classnames';

const ROUTES_WITH_MORATORIUM_BANNER = [
    "/loc/splash",
    "/hp/splash",
    "/rh/splash",
    "/"
  ];

const MoratoriumBanner = ( props:{ pathname?: string } ) => {

    const includeBanner = props.pathname && (ROUTES_WITH_MORATORIUM_BANNER.includes(props.pathname));
    
    const [isVisible, setVisibility] = useState(true);

    return (includeBanner ? 
    <section className={classnames("jf-moratorium-banner","hero","is-warning", "is-small", !isVisible && "is-hidden")}>
        <div className="hero-body">
        <div className="container">
            <SimpleProgressiveEnhancement>
                <button className="delete is-medium is-pulled-right" onClick = {() => setVisibility(false)} />
            </SimpleProgressiveEnhancement>
            <p>
                <span className="has-text-weight-bold">COVID-19 Update: </span>
                JustFix.nyc remains in operation, and we are adapting our products to match new rules put in place during the Covid-19 public health crisis. 
                Thanks to organizing from tenant leaders, renters now have stronger protections during this time, including a full halt on eviction cases. 
                {' '}<a href="https://www.righttocounselnyc.org/moratorium_faq" target="_blank" rel="noopener noreferrer">
                    <span className="has-text-weight-bold">Learn more</span>
                </a>
            </p>
        </div>
        </div>
    </section> : <></>
    );
}

  export default MoratoriumBanner;