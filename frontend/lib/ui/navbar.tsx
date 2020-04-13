import React, { SyntheticEvent } from "react";
import { Link } from "react-router-dom";
import classnames from "classnames";

import autobind from "autobind-decorator";
import { AriaExpandableButton } from "./aria";
import { bulmaClasses } from "./bulma";
import { AppContextType, withAppContext } from "../app-context";
import { ga } from "../analytics/google-analytics";

type Dropdown = "developer" | "all";

export type NavbarProps = AppContextType & {
  /**
   * A component to render the branding at the beginning of the navbar.
   * If omitted, the navbar will have no branding.
   */
  brandComponent?: React.ComponentType<{}>;

  /**
   * A component to render any additional menu items at the end of
   * the navbar. If omitted, the navbar won't have any additional
   * menu items.
   */
  menuItemsComponent?: React.ComponentType<{}>;
};

interface NavbarState {
  currentDropdown: Dropdown | null;
  isHamburgerOpen: boolean;
}

class NavbarWithoutAppContext extends React.Component<
  NavbarProps,
  NavbarState
> {
  navbarRef: React.RefObject<HTMLDivElement>;

  constructor(props: NavbarProps) {
    super(props);
    if (props.session.isSafeModeEnabled) {
      this.state = { currentDropdown: "all", isHamburgerOpen: true };
    } else {
      this.state = { currentDropdown: null, isHamburgerOpen: false };
    }
    this.navbarRef = React.createRef();
  }

  toggleDropdown(dropdown: Dropdown) {
    ga("send", "event", "dropdown", "toggle", dropdown);
    this.setState((state) => ({
      currentDropdown: state.currentDropdown === dropdown ? null : dropdown,
      isHamburgerOpen: false,
    }));
  }

  @autobind
  toggleHamburger() {
    ga("send", "event", "hamburger", "toggle");
    this.setState((state) => ({
      currentDropdown: null,
      isHamburgerOpen: !state.isHamburgerOpen,
    }));
  }

  @autobind
  handleFocus(e: FocusEvent) {
    if (
      (this.state.currentDropdown || this.state.isHamburgerOpen) &&
      this.navbarRef.current &&
      e.target instanceof Node &&
      !this.navbarRef.current.contains(e.target)
    ) {
      this.setState({
        currentDropdown: null,
        isHamburgerOpen: false,
      });
    }
  }

  componentDidMount() {
    window.addEventListener("focus", this.handleFocus, true);
    window.addEventListener("resize", this.handleResize, false);
  }

  componentWillUnmount() {
    window.removeEventListener("focus", this.handleFocus, true);
    window.removeEventListener("resize", this.handleResize, false);
  }

  isDropdownActive(dropdown: Dropdown) {
    return (
      this.state.currentDropdown === dropdown ||
      this.state.currentDropdown === "all"
    );
  }

  @autobind
  handleResize() {
    this.setState({
      currentDropdown: null,
      isHamburgerOpen: false,
    });
  }

  @autobind
  handleShowSafeModeUI(e: SyntheticEvent) {
    e.preventDefault();
    window.SafeMode.showUI();
  }

  renderDevMenu(): JSX.Element | null {
    const { server, session, siteRoutes } = this.props;
    const { state } = this;

    if (!server.debug) return null;

    return (
      <NavbarDropdown
        name="Developer"
        isHamburgerOpen={state.isHamburgerOpen}
        isActive={this.isDropdownActive("developer")}
        onToggle={() => this.toggleDropdown("developer")}
      >
        {!DISABLE_WEBPACK_ANALYZER && (
          <a
            className="navbar-item"
            href={`${server.staticURL}frontend/report.html`}
          >
            Webpack analysis
          </a>
        )}
        <a className="navbar-item" href="/graphiql">
          GraphiQL
        </a>
        <a className="navbar-item" href="/loc/example.pdf">
          Example PDF
        </a>
        <a
          className="navbar-item"
          href="https://github.com/JustFixNYC/tenants2"
        >
          GitHub
        </a>
        {!session.isSafeModeEnabled && (
          <a
            className="navbar-item"
            href="#"
            onClick={this.handleShowSafeModeUI}
          >
            Show safe mode UI
          </a>
        )}
        <Link className="navbar-item" to={siteRoutes.dev.home}>
          More tools&hellip;
        </Link>
      </NavbarDropdown>
    );
  }

  renderNavbarBrand(): JSX.Element {
    const { navbarLabel } = this.props.server;
    const { state } = this;
    const Brand = this.props.brandComponent;

    return (
      <div className="navbar-brand">
        {Brand && <Brand />}
        {navbarLabel && (
          <div className="navbar-item jf-navbar-label">
            <span className="tag is-warning">{navbarLabel}</span>
          </div>
        )}
        <AriaExpandableButton
          className={bulmaClasses(
            "navbar-burger",
            state.isHamburgerOpen && "is-active"
          )}
          isExpanded={state.isHamburgerOpen}
          aria-label="menu"
          onToggle={this.toggleHamburger}
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </AriaExpandableButton>
      </div>
    );
  }

  render() {
    const { state } = this;
    const { session, server } = this.props;
    const navClass = classnames(
      "navbar",
      !session.isSafeModeEnabled && "is-fixed-top"
    );
    const MenuItems = this.props.menuItemsComponent;

    return (
      <nav className={navClass} ref={this.navbarRef}>
        <div className="container">
          {this.renderNavbarBrand()}
          <div
            className={bulmaClasses(
              "navbar-menu",
              state.isHamburgerOpen && "is-active"
            )}
          >
            <div className="navbar-end">
              {MenuItems && <MenuItems />}
              {session.isStaff && (
                <a className="navbar-item" href={server.adminIndexURL}>
                  Admin
                </a>
              )}
              {this.renderDevMenu()}
            </div>
          </div>
        </div>
      </nav>
    );
  }
}

const Navbar = withAppContext(NavbarWithoutAppContext);

export default Navbar;

interface NavbarDropdownProps {
  name: string;
  children: any;
  isHamburgerOpen: boolean;
  isActive: boolean;
  onToggle: () => void;
}

export function NavbarDropdown(props: NavbarDropdownProps): JSX.Element {
  // If the hamburger menu is open, our navbar-link is just
  // inert text; but if it's closed and we're on desktop, it's an
  // interactive menu toggle button. Kind of odd.
  let link = props.isHamburgerOpen ? (
    <a className="navbar-link">{props.name}</a>
  ) : (
    <AriaExpandableButton
      className="navbar-link"
      isExpanded={props.isActive}
      onToggle={props.onToggle}
    >
      {props.name}
    </AriaExpandableButton>
  );

  return (
    <div
      className={bulmaClasses(
        "navbar-item",
        "has-dropdown",
        props.isActive && "is-active"
      )}
    >
      {link}
      <div className="navbar-dropdown">{props.children}</div>
    </div>
  );
}