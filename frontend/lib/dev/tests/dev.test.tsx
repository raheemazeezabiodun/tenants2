import React from "react";

import { AppTesterPal } from "../../tests/app-tester-pal";
import DevRoutes from "../dev";
import JustfixRoutes from "../../justfix-routes";

describe("development pages", () => {
  afterEach(AppTesterPal.cleanup);

  it("shows development tools home", () => {
    const pal = new AppTesterPal(<DevRoutes />, {
      url: "/dev",
    });
    pal.clickButtonOrLink(/examples\/loading-page/);
  });

  it("shows DDO dev page", () => {
    const pal = new AppTesterPal(<DevRoutes />, {
      url: JustfixRoutes.dev.examples.ddo,
    });
    pal.rr.getByText("Submit");
  });

  it("shows mapbox page", () => {
    const pal = new AppTesterPal(<DevRoutes />, {
      url: JustfixRoutes.dev.examples.mapbox,
    });
    pal.rr.getByText(/Example Mapbox page/i);
  });
});
