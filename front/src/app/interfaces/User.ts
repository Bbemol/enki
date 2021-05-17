import { Contact } from './Contact';

export interface User {
  first_name?: string;
  last_name?: string;
  position?: {
    group: {
      label: string;
    };
    position: {
      label: string;
    };
  };
  attributes?: {
    fonction?: string;
  };
  location: string;
  location_id: string;
  fullname?: string;
  contacts: Contact[];
  uuid: string;
}
