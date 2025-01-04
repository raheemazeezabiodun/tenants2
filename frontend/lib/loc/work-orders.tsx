import React from "react";

import Page from "../ui/page";
import { SessionUpdatingFormSubmitter } from "../forms/session-updating-form-submitter";
import { WorkOrderTicketsMutation } from "../queries/WorkOrderTicketsMutation";
import { TextualFormField, CheckboxFormField } from "../forms/form-fields";
import { ProgressButtons } from "../ui/buttons";
import { MiddleProgressStep } from "../progress/progress-step-route";
import { Formset } from "../forms/formset";

type TicketNumber = {
  ticketNumber: string;
};

type InitialState = {
  ticketNumbers: TicketNumber[];
  noTicket: boolean;
};

const MAXIMUM_TICKETS: number = 10;

function labelForTicketNumbers(i: number): string {
  let word: string = "Work order ticket number";
  return i > 0 ? word + ` #${i + 1}` : word;
}

function getInitialState(
  ticketNumbers: string[],
  hasInitiatedWorkOrder: boolean
): InitialState {
  return {
    ticketNumbers: ticketNumbers.map((item) => ({ ticketNumber: item })),
    noTicket: hasInitiatedWorkOrder ? ticketNumbers.length == 0 : false,
  };
}

function userReachedMaxTicket(ticketNumbers: []): boolean {
  return ticketNumbers.length == MAXIMUM_TICKETS;
}

const WorkOrdersPage = MiddleProgressStep((props) => {
  return (
    <Page title="Work order repairs ticket">
      <div>
        <h1 className="title is-4 is-spaced">Work order repairs ticket</h1>
        <p className="subtitle is-6">
          Enter at least one work ticket number. We’ll include these in your
          letter so management can see the issues you’ve already reported.{" "}
        </p>
        <SessionUpdatingFormSubmitter
          mutation={WorkOrderTicketsMutation}
          initialState={(session) =>
            getInitialState(session.workOrder, session.hasInitiatedWorkOrder)
          }
          onSuccessRedirect={props.nextStep}
        >
          {(ctx) => (
            <>
              {console.log(ctx)}
              <Formset
                {...ctx.formsetPropsFor("ticketNumbers")}
                maxNum={MAXIMUM_TICKETS}
                emptyForm={{ ticketNumber: "" }}
                extra={1}
              >
                {(formsetCtx, i) => (
                  <TextualFormField
                    label={labelForTicketNumbers(i)}
                    {...formsetCtx.fieldPropsFor("ticketNumber")}
                    isDisabled={ctx.options.currentState.noTicket}
                  />
                )}
              </Formset>
              <CheckboxFormField
                {...ctx.fieldPropsFor("noTicket")}
                onChange={(value) => {
                  ctx.options.setField("noTicket", value);
                  ctx.options.setField("ticketNumbers", []);
                }}
              >
                I don't have a ticket number
              </CheckboxFormField>
              {userReachedMaxTicket(ctx.options.currentState.ticketNumbers) && (
                <p>
                  The Maximum number of tickets you can enter is{" "}
                  {MAXIMUM_TICKETS}
                </p>
              )}
              <ProgressButtons
                back={props.prevStep}
                isLoading={ctx.isLoading}
              />
            </>
          )}
        </SessionUpdatingFormSubmitter>
      </div>
    </Page>
  );
});

export default WorkOrdersPage;
