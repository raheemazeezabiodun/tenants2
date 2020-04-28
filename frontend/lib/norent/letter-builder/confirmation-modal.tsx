import React from "react";
import { Modal, BackOrUpOneDirLevel } from "../../ui/modal";
import { Link } from "react-router-dom";

type NorentConfirmationModalProps = {
  nextStep: string;
  children: React.ReactNode;
  title: string;
};

/**
 * A modal to use when our verification of the user's latest form input
 * differs from their input: for example, if we think an address is
 * undeliverable, or if we think that something the user wrote may
 * be mis-spelled.
 *
 * This modal is expected to be at a route that is one directory level
 * deeper than the page it's overlaid atop. For instance, if the page
 * it's on is at `/foo/bar`, then the modal itself can be at
 * `/foo/bar/confirmation-modal`.
 */
export const NorentConfirmationModal: React.FC<NorentConfirmationModalProps> = (
  props
) => {
  return (
    <Modal
      title={props.title}
      withHeading
      onCloseGoTo={BackOrUpOneDirLevel}
      render={(ctx) => (
        <>
          {props.children}
          <div className="buttons jf-two-buttons">
            <Link
              {...ctx.getLinkCloseProps()}
              className="jf-is-back-button button is-medium"
            >
              No
            </Link>
            <Link
              to={props.nextStep}
              className="button is-primary is-medium jf-is-next-button"
            >
              Yes
            </Link>
          </div>
        </>
      )}
    />
  );
};