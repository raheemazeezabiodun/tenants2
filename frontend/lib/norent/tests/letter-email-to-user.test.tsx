import React from "react";
import { AppTesterPal } from "../../tests/app-tester-pal";
import { NorentLetterEmailToUser } from "../letter-email-to-user";
import { NorentLinguiI18n } from "../site";
import { preloadLingui } from "../../tests/lingui-preloader";

beforeAll(preloadLingui(NorentLinguiI18n));

describe("NorentLetterEmailToUser", () => {
  it("works", () => {
    const pal = new AppTesterPal(<NorentLetterEmailToUser />, {
      session: { firstName: "Boop" },
    });
    expect(pal.rr.container).toMatchSnapshot();
  });
});
