import React from "react";
import JustfixRoutes from "../../justfix-routes";
import { AppTesterPal } from "../../tests/app-tester-pal";
import LetterOfComplaintRoutes from "../letter-of-complaint";
import { LetterRequestMutation } from "../../queries/LetterRequestMutation";
import { LetterRequestMailChoice } from "../../queries/globalTypes";
import { newSb } from "../../tests/session-builder";

const sb = newSb().withLoggedInJustfixUser();

const PRE_EXISTING_LETTER_REQUEST = {
  mailChoice: LetterRequestMailChoice.WE_WILL_MAIL,
  updatedAt: "blahh",
  trackingNumber: "",
  letterSentAt: null,
};

describe("landlord details page", () => {
  async function clickButtonAndExpectChoice(
    pal: AppTesterPal,
    matcher: RegExp,
    mailChoice: LetterRequestMailChoice
  ) {
    pal.clickButtonOrLink(matcher);
    const updatedAt = "2018-01-01Tblahtime";
    const extra = { trackingNumber: "", letterSentAt: null };
    pal
      .withFormMutation(LetterRequestMutation)
      .expect({ mailChoice })
      .respondWith({
        errors: [],
        session: { letterRequest: { updatedAt, mailChoice, ...extra } },
      });

    await pal.rt.waitFor(() =>
      pal.rr.getByText(/your letter of complaint .*/i)
    );
    const { mock } = pal.appContext.updateSession;
    expect(mock.calls).toHaveLength(1);
    expect(mock.calls[0][0]).toEqual({
      letterRequest: { updatedAt, mailChoice, ...extra },
    });
  }

  it("works when user chooses to mail the letter themselves", async () => {
    const pal = new AppTesterPal(<LetterOfComplaintRoutes />, {
      url: JustfixRoutes.locale.loc.preview,
      session: sb.with({
        letterRequest: PRE_EXISTING_LETTER_REQUEST,
      }).value,
    });
    clickButtonAndExpectChoice(
      pal,
      /mail this myself/i,
      LetterRequestMailChoice.USER_WILL_MAIL
    );
  });

  it("works when user wants us to mail the letter", async () => {
    const pal = new AppTesterPal(<LetterOfComplaintRoutes />, {
      url: JustfixRoutes.locale.loc.preview,
      session: sb.with({
        letterRequest: PRE_EXISTING_LETTER_REQUEST,
      }).value,
    });
    pal.clickButtonOrLink(/looks good to me/i);
    await pal.rt.waitFor(() => pal.getDialogWithLabel(/ready to go/i));

    clickButtonAndExpectChoice(
      pal,
      /mail my letter/i,
      LetterRequestMailChoice.WE_WILL_MAIL
    );
  });
});
