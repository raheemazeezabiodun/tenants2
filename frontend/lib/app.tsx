import React, { RefObject } from "react";
import ReactDOM from "react-dom";
import autobind from "autobind-decorator";
import {
  BrowserRouter,
  RouteComponentProps,
  withRouter,
} from "react-router-dom";
import loadable, { loadableReady } from "@loadable/component";

import GraphQlClient from "./networking/graphql-client";

import { AllSessionInfo } from "./queries/AllSessionInfo";
import {
  AppServerInfo,
  AppContext,
  AppContextType,
  AppLegacyFormSubmission,
  AppSiteRoutes,
} from "./app-context";
import { ErrorBoundary } from "./error-boundary";
import { isModalRoute } from "./util/route-util";
import { AriaAnnouncer } from "./ui/aria";
import { trackPageView, ga } from "./analytics/google-analytics";
import { Action } from "history";
import {
  smoothlyScrollToTopOfPage,
  smoothlyScrollToLocation,
} from "./util/scrolling";
import {
  HistoryBlockerManager,
  getNavigationConfirmation,
} from "./forms/history-blocker";
import { HelmetProvider } from "react-helmet-async";
import { browserStorage } from "./browser-storage";
import { areAnalyticsEnabled } from "./analytics/analytics";
import { default as JustfixRoutes } from "./routes";
import { NorentRoutes } from "./norent/routes";

// Note that these don't need any special fallback loading screens
// because they will never need to be dynamically loaded on the
// client-side, as they represent entirely different websites.
// We're just using our infrastructure for code splitting here.
const LoadableJustfixSite = loadable(() => import("./justfix-site"));
const LoadableNorentSite = loadable(() => import("./norent/site"));

export type AppSiteProps = RouteComponentProps & {
  ref?: React.Ref<HTMLDivElement>;
};

export interface AppProps {
  /** The initial URL to render on page load. */
  initialURL: string;

  /**
   * The locale the user is on. This can be an empty string to
   * indicate that localization is disabled, or an ISO 639-1
   * code such as 'en' or 'es'.
   */
  locale: string;

  /** The initial session state the App was started with. */
  initialSession: AllSessionInfo;

  /** Metadata about the server. */
  server: AppServerInfo;

  /**
   * If a form was manually submitted via a browser that doesn't support JS,
   * the server will have processed the POST data for us and put the
   * results here.
   */
  legacyFormSubmission?: AppLegacyFormSubmission;

  /**
   * If provided, this will *not* render a whole website, but instead just
   * the single child wrapped in an AppContext.
   */
  children?: JSX.Element;
}

export type AppPropsWithRouter = AppProps & RouteComponentProps<any>;

interface AppState {
  /**
   * The current session state of the App, which can
   * be different from the initial session if e.g. the user
   * has logged out since the initial page load.
   */
  session: AllSessionInfo;
}

export class AppWithoutRouter extends React.Component<
  AppPropsWithRouter,
  AppState
> {
  gqlClient: GraphQlClient;
  pageBodyRef: RefObject<HTMLDivElement>;

  constructor(props: AppPropsWithRouter) {
    super(props);
    this.gqlClient = new GraphQlClient(
      props.server.batchGraphQLURL,
      props.initialSession.csrfToken
    );
    this.state = {
      session: props.initialSession,
    };
    this.pageBodyRef = React.createRef();
  }

  @autobind
  fetchWithoutErrorHandling(query: string, variables?: any): Promise<any> {
    return this.gqlClient.fetch(query, variables);
  }

  @autobind
  fetch(query: string, variables?: any): Promise<any> {
    return this.gqlClient.fetch(query, variables).catch((e) => {
      this.handleFetchError(e);
      throw e;
    });
  }

  @autobind
  handleFetchError(e: Error) {
    window.alert(
      `Unfortunately, a network error occurred. Please try again later.`
    );
    // We're going to track exceptions in GA because we want to know how frequently
    // folks are experiencing them. However, we won't report the errors
    // to a service like Rollbar because these errors are only worth investigating
    // if they're server-side, and we've already got error reporting configured
    // over there.
    ga("send", "exception", {
      exDescription: e.message,
      exFatal: false,
    });
    console.error(e);
  }

  @autobind
  handleSessionChange(updates: Partial<AllSessionInfo>) {
    this.setState((state) => ({ session: { ...state.session, ...updates } }));
  }

  handleFocusOnHash(hash: string) {
    const element = document.getElementById(hash.slice(1));
    if (element) {
      element.focus({ preventScroll: true });
    }
  }

  handleScrollToHash(hash: string) {
    const element = document.getElementById(hash.slice(1));
    if (element) {
      smoothlyScrollToLocation(element);
    }
  }

  handleFocusDuringPathnameChange(
    prevPathname: string,
    pathname: string,
    hash: string
  ) {
    // Modals handle focus changes themselves, so don't manage focus if
    // we're moving to or from a modal.
    if (!isModalRoute(prevPathname, pathname)) {
      if (hash.length > 1) {
        this.handleFocusOnHash(hash);
        return;
      }
      // This isn't a modal, so focus on the page's body to ensure
      // focus isn't lost in the page transition.
      const body = this.pageBodyRef.current;
      if (body) {
        // We're using call() here to work around the fact that TypeScript doesn't
        // currently have the typings for this newer call signature for focus():
        // https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/focus
        //
        // We want to prevent the browser from scrolling to the focus target
        // because we're managing scrolling ourselves.
        body.focus.call(body, { preventScroll: true });
      }
    }
  }

  handleScrollPositionDuringPathnameChange(
    prevPathname: string,
    pathname: string,
    hash: string,
    action: Action
  ) {
    // We don't need to worry about scroll position when transitioning into a modal, and
    // we only need to adjust it when the user is navigating to a new page. This means
    // we need to watch for history pushes (regular link clicks and such) as well
    // as replaces (e.g. when a link goes to '/foo' which immediately redirects to
    // '/foo/bar').
    if (
      !isModalRoute(pathname) &&
      (action === "PUSH" || action === "REPLACE")
    ) {
      if (hash.length > 1) {
        this.handleScrollToHash(hash);
      } else {
        smoothlyScrollToTopOfPage();
      }
    }
  }

  handlePathnameChange(
    prevPathname: string,
    prevHash: string,
    pathname: string,
    hash: string,
    action: Action
  ) {
    if (prevPathname !== pathname) {
      trackPageView(pathname);
      this.handleFocusDuringPathnameChange(prevPathname, pathname, hash);
      this.handleScrollPositionDuringPathnameChange(
        prevPathname,
        pathname,
        hash,
        action
      );
    } else if (prevHash !== hash) {
      this.handleFocusOnHash(hash);
      this.handleScrollToHash(hash);
    }
  }

  handleLogin() {
    const { userId, firstName, isStaff } = this.state.session;
    if (isStaff && areAnalyticsEnabled()) {
      // There's no way to disable analytics without reloading the page,
      // so just reload it.
      window.location.reload();
    }
    if (window.FS && userId !== null) {
      // FullStory ignores '1' as a user ID because it might be unintentional,
      // but that's actually a valid user ID for our purposes, so we'll munge
      // our user IDs a bit so FullStory always uses them.
      const uid = `user:${userId}`;

      window.FS.identify(uid, {
        displayName: `${firstName || ""} (#${userId})`,
      });
    }
  }

  handleLogout() {
    // We're not going to bother telling FullStory that the user logged out,
    // because we don't really want it associating the current user with a
    // brand-new anonymous user (as FullStory's priced plans have strict limits
    // on the number of user sessions they can support).
  }

  componentDidMount() {
    if (this.state.session.userId !== null) {
      this.handleLogin();
    }
  }

  componentDidUpdate(prevProps: AppPropsWithRouter, prevState: AppState) {
    if (prevState.session.userId !== this.state.session.userId) {
      if (this.state.session.userId === null) {
        this.handleLogout();
      } else {
        this.handleLogin();
      }
    }
    if (prevState.session.csrfToken !== this.state.session.csrfToken) {
      this.gqlClient.csrfToken = this.state.session.csrfToken;
      browserStorage.clear();
    }
    this.handlePathnameChange(
      prevProps.location.pathname,
      prevProps.location.hash,
      this.props.location.pathname,
      this.props.location.hash,
      this.props.history.action
    );
  }

  getAppContext(): AppContextType {
    return {
      server: this.props.server,
      session: this.state.session,
      siteRoutes: this.getSiteRoutes(),
      fetch: this.fetch,
      fetchWithoutErrorHandling: this.fetchWithoutErrorHandling,
      updateSession: this.handleSessionChange,
      legacyFormSubmission: this.props.legacyFormSubmission,
    };
  }

  get isLoggedIn(): boolean {
    return !!this.state.session.phoneNumber;
  }

  getSiteRoutes(): AppSiteRoutes {
    switch (this.props.server.siteType) {
      case "JUSTFIX":
        return JustfixRoutes;
      case "NORENT":
        return NorentRoutes;
    }
  }

  getSiteComponent(): React.ComponentType<AppSiteProps> {
    switch (this.props.server.siteType) {
      case "JUSTFIX":
        return LoadableJustfixSite;
      case "NORENT":
        return LoadableNorentSite;
    }
  }

  render() {
    if (this.props.children) {
      return (
        <AppContext.Provider
          value={this.getAppContext()}
          children={this.props.children}
        />
      );
    }

    const Site = this.getSiteComponent();

    return (
      <ErrorBoundary debug={this.props.server.debug}>
        <HistoryBlockerManager>
          <AppContext.Provider value={this.getAppContext()}>
            <AriaAnnouncer>
              <Site {...this.props} ref={this.pageBodyRef} />
            </AriaAnnouncer>
          </AppContext.Provider>
        </HistoryBlockerManager>
      </ErrorBoundary>
    );
  }
}

export const App = withRouter(AppWithoutRouter);

export function startApp(container: Element, initialProps: AppProps) {
  const el = (
    <HelmetProvider>
      <BrowserRouter getUserConfirmation={getNavigationConfirmation}>
        <App {...initialProps} />
      </BrowserRouter>
    </HelmetProvider>
  );
  if (container.children.length) {
    // Initial content has been generated server-side, so preload any
    // necessary JS bundles and bind to the DOM.
    loadableReady(() => {
      ReactDOM.hydrate(el, container);
    });
  } else {
    // No initial content was provided, so generate a DOM from scratch.
    ReactDOM.render(el, container);
  }
}
