import React from 'react';
import ReactDOM from 'react-dom';
import autobind from 'autobind-decorator';
import { BrowserRouter, Switch, Route } from 'react-router-dom';
import Loadable from 'react-loadable';

import GraphQlClient from './graphql-client';

import { fetchLogoutMutation } from './queries/LogoutMutation';
import { fetchLoginMutation } from './queries/LoginMutation';
import { AppSessionInfo } from './app-session-info';
import { AppServerInfo } from './app-server-info';
import { NotFound } from './not-found';


export interface AppProps {
  /** The initial URL to render on page load. */
  initialURL: string;

  /** The initial session state the App was started with. */
  initialSession: AppSessionInfo;

  /** Metadata about the server. */
  server: AppServerInfo;
}

interface AppState {
  /**
   * The current session state of the App, which can
   * be different from the initial session if e.g. the user
   * has logged out since the initial page load.
   */
  session: AppSessionInfo;
}

const LoadableIndexPage = Loadable({
  loader: () => import(/* webpackChunkName: "index-page" */ './index-page'),
  loading() {
    return <div>Loading...</div>;
  }
});

export class App extends React.Component<AppProps, AppState> {
  gqlClient: GraphQlClient;

  constructor(props: AppProps) {
    super(props);
    this.gqlClient = new GraphQlClient(
      props.server.batchGraphQLURL,
      props.initialSession.csrfToken
    );
    this.state = { session: props.initialSession };
  }

  @autobind
  handleFetchError(e: Error) {
    console.error(e);
    window.alert(`Alas, a fatal error occurred: ${e.message}`);
  }

  @autobind
  handleLogout() {
    fetchLogoutMutation(this.gqlClient.fetch).then((result) => {
      if (result.logout.ok) {
        this.setState({
          session: {
            phoneNumber: null,
            csrfToken: result.logout.csrfToken
          },
        });
        return;
      }
      throw new Error('Assertion failure, logout should always be ok');
    }).catch(this.handleFetchError);
  }

  @autobind
  handleLoginSubmit(phoneNumber: string, password: string) {
    fetchLoginMutation(this.gqlClient.fetch, {
      phoneNumber: phoneNumber,
      password: password
    }).then(result => {
      if (result.login.ok) {
        this.setState({
          session: {
            phoneNumber,
            csrfToken: result.login.csrfToken
          }
        });
      } else {
        window.alert("Invalid phone number or password.");
      }
    }).catch(this.handleFetchError);
  }

  componentDidUpdate(prevProps: AppProps, prevState: AppState) {
    if (prevProps !== this.props) {
      throw new Error('Assertion failure, props are not expected to change');
    }
    if (prevState.session.csrfToken !== this.state.session.csrfToken) {
      this.gqlClient.csrfToken = this.state.session.csrfToken;
    }
  }

  render() {
    return (
      <Switch>
        <Route path="/" exact>
          <LoadableIndexPage
           gqlClient={this.gqlClient}
           server={this.props.server}
           session={this.state.session}
           onFetchError={this.handleFetchError}
           onLogout={this.handleLogout}
           onLoginSubmit={this.handleLoginSubmit}
          />
        </Route>
        <Route path="/about" exact>
          <p>This is another page.</p>
        </Route>
        <Route render={NotFound} />
      </Switch>
    );
  }
}

export function startApp(container: Element, initialProps: AppProps) {
  const el = (
    <BrowserRouter>
      <App {...initialProps}/>
    </BrowserRouter>
  );
  if (container.children.length) {
    // Initial content has been generated server-side, so preload any
    // necessary JS bundles and bind to the DOM.
    Loadable.preloadReady().then(() => {
      ReactDOM.hydrate(el, container);
    }).catch(e => {
      window.alert("Loadable.preloadReady() failed!");
    });
  } else {
    // No initial content was provided, so generate a DOM from scratch.
    ReactDOM.render(el, container);
  }
}
