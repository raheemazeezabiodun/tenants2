import React from "react";
import { Route } from "react-router-dom";

import { waitFor } from "@testing-library/react";

import { AppTesterPal } from "../../tests/app-tester-pal";
import LaLetterBuilderSite from "../site";

describe("LaLetterBuilderSite", () => {
  const route = (
    <Route render={(props) => <LaLetterBuilderSite {...props} />} />
  );

  it("renders 404 page", () => {
    const pal = new AppTesterPal(route, { url: "/blarg" });
    waitFor(() => pal.rr.getByText(/doesn't seem to exist/i));
  });

  it("renders home page", () => {
    const pal = new AppTesterPal(route, { url: "/en/" });
    waitFor(() =>
      pal.rr.getByText(
        /This is a test localization message for LaLetterBuilder/i
      )
    );
  });
});
