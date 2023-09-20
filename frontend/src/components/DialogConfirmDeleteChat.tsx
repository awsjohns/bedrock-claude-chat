import React from "react";
import { BaseProps } from "../@types/common";
import { ConversationMeta } from "../@types/conversation";
import Button from "./Button";
import ModalDialog from "./ModalDialog";

type Props = BaseProps & {
  isOpen: boolean;
  target?: ConversationMeta;
  onDelete: (conversationId: string) => void;
  onClose: () => void;
};

const DialogConfirmDeleteChat: React.FC<Props> = (props) => {
  return (
    <ModalDialog {...props} title="Delete Confirmation">
      <div>
        Chat
        <span className="font-bold">「{props.target?.title}」</span>
        Do you want to delete it?
      </div>

      <div className="mt-4 flex justify-end gap-2">
        <Button
          onClick={props.onClose}
          className="bg-transparent text-aws-font-color p-2"
        >
          Cancel
        </Button>
        <Button
          onClick={() => {
            props.onDelete(props.target?.id ?? "");
          }}
          className="bg-red-500 text-aws-font-color-white p-2"
        >
          delete
        </Button>
      </div>
    </ModalDialog>
  );
};

export default DialogConfirmDeleteChat;
