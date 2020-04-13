import React, { useContext } from "react";
import Navbar from "./ui/navbar";
import { Link } from "react-router-dom";
import { AppContext } from "./app-context";
import Routes from "./routes";
import { StaticImage } from "./ui/static-image";

const JustfixBrand: React.FC<{}> = () => {
  const { onboardingInfo } = useContext(AppContext).session;
  const to = onboardingInfo
    ? Routes.locale.homeWithSearch(onboardingInfo)
    : Routes.locale.home;

  return (
    <Link className="navbar-item" to={to}>
      <StaticImage ratio="is-128x128" src="frontend/img/logo.png" alt="Home" />
    </Link>
  );
};

const JustfixMenuItems: React.FC<{}> = () => {
  const { session } = useContext(AppContext);

  return (
    <>
      {session.onboardingInfo && (
        <Link
          className="navbar-item"
          to={Routes.locale.homeWithSearch(session.onboardingInfo)}
        >
          Take action
        </Link>
      )}
      {session.phoneNumber ? (
        <Link className="navbar-item" to={Routes.locale.logout}>
          Sign out
        </Link>
      ) : (
        <Link className="navbar-item" to={Routes.locale.login}>
          Sign in
        </Link>
      )}
      <Link className="navbar-item" to={Routes.locale.help}>
        Help
      </Link>
    </>
  );
};

export const JustfixNavbar: React.FC<{}> = () => {
  return (
    <Navbar
      brandComponent={JustfixBrand}
      menuItemsComponent={JustfixMenuItems}
    />
  );
};