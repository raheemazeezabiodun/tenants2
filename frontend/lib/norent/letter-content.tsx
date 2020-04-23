import React, { useContext } from "react";
import { QueryLoader } from "../networking/query-loader";
import { NorentLetterContentQuery } from "../queries/NorentLetterContentQuery";
import { LetterStaticPage } from "../static-page/letter-static-page";
import { AppContext } from "../app-context";
import { AllSessionInfo } from "../queries/AllSessionInfo";
import { friendlyDate, assertNotNull } from "../util/util";
import { formatPhoneNumber } from "../forms/phone-number-form-field";
import {
  EmailSubject,
  EmailStaticPage,
} from "../static-page/email-static-page";

export type NorentLetterContentProps = {
  firstName: string;
  lastName: string;
  street: string;
  city: string;
  state: string;
  zipCode: string;
  aptNumber: string;
  email: string;
  phoneNumber: string;
  landlordName: string;
  landlordPrimaryLine: string;
  landlordCity: string;
  landlordState: string;
  landlordZipCode: string;
  landlordEmail: string;
  paymentDate: GraphQLDate;
};

const LandlordName: React.FC<NorentLetterContentProps> = (props) => (
  <>{props.landlordName.toUpperCase()}</>
);

const FullName: React.FC<NorentLetterContentProps> = (props) => (
  <>
    {props.firstName} {props.lastName}
  </>
);

const LetterTitle: React.FC<NorentLetterContentProps> = (props) => (
  /*
   * We originally had a <br> in this <h1>, but React self-closes the
   * tag as <br/>, which WeasyPrint doesn't seem to like, so we'll
   * include an actual newline and set the style to preserve whitespace.
   */
  <h1 className="has-text-right" style={{ whiteSpace: "pre-wrap" }}>
    <span className="is-uppercase">Notice of non-payment of rent</span>
    {"\n"}
    at {props.street}, {props.city}, {props.state} {props.zipCode}
  </h1>
);

const PaymentDate: React.FC<{ paymentDate: GraphQLDate }> = (props) => (
  // Oy, the payment date is in midnight UTC time, and we explicitly want
  // to *not* convert it to any other time zone, otherwise it may
  // appear as a different date.
  <>{friendlyDate(new Date(props.paymentDate), "UTC")}</>
);

const LetterHeading: React.FC<NorentLetterContentProps> = (props) => (
  <dl className="jf-letter-heading">
    <dt>To</dt>
    <dd>
      <LandlordName {...props} />
      <br />
      {props.landlordPrimaryLine}
      <br />
      {props.landlordCity}, {props.landlordState} {props.landlordZipCode}
    </dd>
    <dt>From</dt>
    <dd>
      <FullName {...props} />
      <br />
      {props.street}
      <br />
      {props.city}, {props.state} {props.zipCode}
      <br />
      {formatPhoneNumber(props.phoneNumber)}
      <br />
      {props.email}
    </dd>
  </dl>
);

const TenantProtections: React.FC<{}> = () => (
  <>
    <p>
      Tenants impacted by the COVID-19 crisis are protected from eviction for
      nonpayment per emergency declaration(s) from:
    </p>
    <ul>
      <li>US Congress, CARES Act (Title IV, Sec. 4024), March 27, 2020</li>
    </ul>
  </>
);

const LetterContentPropsFromSession: React.FC<{
  children: (lcProps: NorentLetterContentProps) => JSX.Element;
}> = ({ children }) => {
  const { session } = useContext(AppContext);
  const lcProps = getNorentLetterContentPropsFromSession(session);

  if (!lcProps) {
    return <p>We don't have enough information to generate a letter yet.</p>;
  }

  return children(lcProps);
};

export const NorentLetterEmail: React.FC<NorentLetterContentProps> = (
  props
) => (
  <>
    <EmailSubject value="My rent payment" />
    <p>
      Dear <LandlordName {...props} />,
    </p>
    <p>
      I am writing to let you know that I am not able to pay my rent starting{" "}
      <PaymentDate {...props} /> because of COVID-19 related reasons. Please see
      the attached letter.
    </p>
    <p>Sincerely,</p>
    <p>
      <FullName {...props} />
    </p>
  </>
);

export const NorentLetterEmailForUser: React.FC<{}> = () => (
  <LetterContentPropsFromSession
    children={(lcProps) => <NorentLetterEmail {...lcProps} />}
  />
);

export const NorentLetterEmailForUserStaticPage: React.FC<{}> = () => (
  <EmailStaticPage>
    <NorentLetterEmailForUser />
  </EmailStaticPage>
);

export const NorentLetterContent: React.FC<NorentLetterContentProps> = (
  props
) => (
  <>
    <LetterTitle {...props} />
    <p className="has-text-right">{friendlyDate(new Date())}</p>
    <LetterHeading {...props} />
    <p>
      Dear <LandlordName {...props} />,
    </p>
    <p>
      This letter is to notify you that I will be unable to pay rent starting on{" "}
      <PaymentDate {...props} /> and until further notice due to loss of income,
      increased expenses, and/or other financial circumstances related to
      COVID-19.
    </p>
    <TenantProtections />
    <p>
      In order to document our communication and to avoid misunderstandings,
      please reply to me via email or text rather than a call or visit.
    </p>
    <p>Thank you for your understanding and cooperation.</p>
    <p className="jf-signature">
      Regards,
      <br />
      <br />
      <FullName {...props} />
    </p>
  </>
);

const NorentLetterStaticPage: React.FC<
  { isPdf?: boolean; title: string } & NorentLetterContentProps
> = ({ isPdf, title, ...props }) => (
  <QueryLoader
    query={NorentLetterContentQuery}
    render={(output) => {
      return (
        <LetterStaticPage title={title} isPdf={isPdf} css={output.letterStyles}>
          <NorentLetterContent {...props} />
        </LetterStaticPage>
      );
    }}
    input={null}
    loading={() => null}
  />
);

function getNorentLetterContentPropsFromSession(
  session: AllSessionInfo
): NorentLetterContentProps | null {
  const onb = session.onboardingInfo;
  const ld = session.landlordDetails;
  if (!(ld && onb)) {
    return null;
  }

  const paymentDate = session.norentLatestRentPeriod?.paymentDate;

  if (!paymentDate) {
    console.log(
      "No latest rent period defined! Please create one in the admin."
    );
    return null;
  }

  const props: NorentLetterContentProps = {
    paymentDate,
    phoneNumber: assertNotNull(session.phoneNumber),
    firstName: assertNotNull(session.firstName),
    lastName: assertNotNull(session.lastName),
    email: assertNotNull(session.email),
    street: onb.address,
    city: onb.city,
    state: onb.state,
    zipCode: onb.zipcode,
    aptNumber: onb.aptNumber,
    landlordName: ld.name,
    landlordPrimaryLine: ld.primaryLine,
    landlordCity: ld.city,
    landlordState: ld.state,
    landlordZipCode: ld.zipCode,
    landlordEmail: ld.email,
  };

  return props;
}

export const NorentLetterForUserStaticPage: React.FC<{ isPdf?: boolean }> = ({
  isPdf,
}) => (
  <LetterContentPropsFromSession
    children={(lcProps) => (
      <NorentLetterStaticPage
        {...lcProps}
        isPdf={isPdf}
        title="Your NoRent.org letter"
      />
    )}
  />
);

export const noRentSampleLetterProps: NorentLetterContentProps = {
  firstName: "Boop",
  lastName: "Jones",
  street: "654 Park Place",
  city: "Brooklyn",
  state: "NY",
  zipCode: "12345",
  aptNumber: "2",
  email: "boop@jones.com",
  phoneNumber: "5551234567",
  landlordName: "Landlordo Calrissian",
  landlordPrimaryLine: "1 Cloud City Drive",
  landlordCity: "Bespin",
  landlordState: "OH",
  landlordZipCode: "41235",
  landlordEmail: "landlordo@calrissian.net",
  paymentDate: "2020-05-01T15:41:37.114Z",
};

export const NorentSampleLetterSamplePage: React.FC<{ isPdf?: boolean }> = ({
  isPdf,
}) => (
  <NorentLetterStaticPage
    {...noRentSampleLetterProps}
    title="Sample NoRent.org letter"
    isPdf={isPdf}
  />
);
