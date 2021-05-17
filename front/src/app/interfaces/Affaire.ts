export interface Affaire {
  uuid: string;
  dateTimeSent: object;
  natureDeFait: string;
  resource?: any;
  coord: Coordinates;
  victims: number;
  address: string;
  evenement_id: string;
}
interface Coordinates {
  lat: number;
  long: number;
}