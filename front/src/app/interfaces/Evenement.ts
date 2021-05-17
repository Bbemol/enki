import { Participant } from './Participant';
import { Message } from './Message';
import { MessageFilter } from './MessageFilter'


export enum EvenementType {
  INCENDIE = "incendie",
  INONDATION = "inondation",
  ATTENTAT = "attentat"
}

export enum EvenementStatus {
  ongoing = "En cours",
  tobegoing = "À venir",
  over = "Terminé"
};
export interface Evenement {
  uuid: string;
  title: string;
  creator: {
    position: {
      group: {
        label: string;
      }
    }
  };
  location_id: string;
  started_at: Date;
  ended_at: string;
  description: string;
  created_at: string;
  closed: boolean;
  user_roles: Participant[];
  messages: Message[];
  filter: MessageFilter;
  status: EvenementStatus;
}

export interface EvenementsHTTP {
  data: Evenement[];
  message: string;
}