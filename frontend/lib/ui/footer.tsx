import React from "react";

export const Footer: React.FC<{}> = () => (
  <footer>
    <div className="container">
      <div className="columns">
        <div className="column is-8">
          <div className="content">
            <p>
              Disclaimer: The information in JustFix.nyc does not constitute
              legal advice and must not be used as a substitute for the advice
              of a lawyer qualified to give advice on legal issues pertaining to
              housing. We can help direct you to free legal services if
              necessary.
            </p>
            <p>JustFix.nyc is a registered 501(c)(3) nonprofit organization.</p>
          </div>
        </div>
        <div className="column is-4 has-text-right content">
          <p>
            Made with NYC ♥ by the team at{" "}
            <a href="https://justfix.nyc">JustFix.nyc</a>
          </p>
        </div>
      </div>
      <div className="columns">
        <div className="column is-8">
          <hr />
          <ul>
            <li>
              <a href="https://www.justfix.nyc/privacy-policy">
                Privacy policy
              </a>
            </li>
            <li>
              <a href="https://www.justfix.nyc/terms-of-use">Terms of use</a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
);
