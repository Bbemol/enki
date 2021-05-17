
export interface Message {
  title: string;
  description: string;
  creator: {
    last_name: string;
    first_name: string;
    position: {
      group_id: string;
      group: {
        label: string;
      },
    },
    uuid: string;
  };
  created_at: string;
  uuid: string;
  tags: any[];
  resources: any[];
  evenement_id: string;
  type: string;
  type_label: string;
  restricted: boolean;
}
