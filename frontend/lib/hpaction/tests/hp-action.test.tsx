import React from "react";

import { AppTesterPal } from "../../tests/app-tester-pal";
import HPActionRoutes, { getHPActionProgressRoutesProps } from "../hp-action";
import { ProgressRoutesTester } from "../../progress/tests/progress-routes-tester";
import JustfixRoutes from "../../justfix-routes";
import { HPUploadStatus } from "../../queries/globalTypes";

const tester = new ProgressRoutesTester(
  getHPActionProgressRoutesProps(),
  "HP Action"
);

tester.defineSmokeTests();

describe("HP Action flow", () => {
  afterEach(AppTesterPal.cleanup);

  it("should show PDF download link on confirmation page", () => {
    const pal = new AppTesterPal(<HPActionRoutes />, {
      url: "/en/hp/confirmation",
      session: {
        latestHpActionPdfUrl: "/boop.pdf",
      },
    });
    const a = pal.rr.getByText(/download/i);
    expect(a.getAttribute("href")).toBe("/boop.pdf");
  });
});

describe("upload status page", () => {
  afterEach(AppTesterPal.cleanup);

  const makePal = (hpActionUploadStatus: HPUploadStatus) =>
    new AppTesterPal(<HPActionRoutes />, {
      url: "/en/hp/wait",
      session: { hpActionUploadStatus },
    });

  it('should show "please wait" when docs are being assembled', () => {
    const pal = makePal(HPUploadStatus.STARTED);
    pal.rr.getByText(/please wait/i);
  });

  it("should redirect to confirmation when docs are ready", () => {
    const pal = makePal(HPUploadStatus.SUCCEEDED);
    expect(pal.history.location.pathname).toBe("/en/hp/confirmation");
  });

  it("should show error page if errors occurred", () => {
    const pal = makePal(HPUploadStatus.ERRORED);
    pal.rr.getByText(/try again/i);
  });

  it("should redirect to beginning if docs are not started", () => {
    const pal = makePal(HPUploadStatus.NOT_STARTED);
    expect(pal.history.location.pathname).toBe("/en/hp/splash");
  });
});

describe("latest step redirector", () => {
  it("returns splash page when user is not logged-in", () => {
    expect(tester.getLatestStep()).toBe(JustfixRoutes.locale.hp.splash);
  });

  it("returns welcome page when user is logged-in", () => {
    expect(tester.getLatestStep({ phoneNumber: "123" })).toBe(
      JustfixRoutes.locale.hp.welcome
    );
  });

  it("returns wait page when user has started document assembly", () => {
    expect(
      tester.getLatestStep({
        hpActionUploadStatus: HPUploadStatus.STARTED,
      })
    ).toBe(JustfixRoutes.locale.hp.waitForUpload);
  });

  it("returns confirmation page when user has generated a PDF", () => {
    expect(
      tester.getLatestStep({
        latestHpActionPdfUrl: "/boop.pdf",
        hpActionUploadStatus: HPUploadStatus.SUCCEEDED,
      })
    ).toBe(JustfixRoutes.locale.hp.confirmation);
  });
});
