import { environment } from 'src/environments/environment';
import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { catchError, map, pluck } from 'rxjs/operators';
import { Affaire, Location, Evenement, EvenementsHTTP, EvenementStatus, Participant, Message, MessageFilter, ToastType } from 'src/app/interfaces';
import { AffairesService } from '../affaires/affaires.service';
import { HTTP_DATA } from '../constants/constants';
import { ToastService } from '../toast/toast.service';

@Injectable({
  providedIn: 'root'
})
export class EvenementsService {

  readonly _evenements = new BehaviorSubject<Evenement[]>([]);
  public evenements$: Observable<Evenement[]>;
  evenementsUrl: string;
  selectedEvenementUUID = new BehaviorSubject<string>('');
  selectedEvenementParticipants = new BehaviorSubject<Participant[]>([]);
  httpOptions: object;
  
  constructor(
    private http: HttpClient,
    private affairesService: AffairesService,
    private toastService: ToastService,
    ) {
      this.evenementsUrl = `${environment.backendUrl}/events`
      this.evenements$ = this._evenements.asObservable();
      this.httpOptions = {
        headers: new HttpHeaders({
          'Content-Type':  'application/json',
        })
      }
  }

  getEvenements(): Evenement[] {
    return this._evenements.getValue();
  }

  getEvenementByID(uuid: string): Evenement {
    return this.getEvenements().filter(evenement => evenement.uuid === uuid)[0];
  }

  private _setEvenements(evenements: Evenement[]): void {
    this._evenements.next(evenements)
  }


  addOrUpdateEvenement(evenementToAdd: Evenement): void {
    let evenements: Evenement[] = this.getEvenements()
    if(!evenementToAdd.filter) {
      evenementToAdd.filter = {
        etablissement: '',
        auteur: '',
        type: '',
        fromDatetime: '',
        toDatetime: '',
      };
    }
    evenementToAdd.started_at = new Date(evenementToAdd.started_at + "Z")
    // if it already exist, then update it
    if (evenements.some(event => event.uuid === evenementToAdd.uuid)) {
      evenements.map(evenement => {
        return evenementToAdd.uuid === evenement.uuid ? evenementToAdd : evenement
      })
    } else {
      // if it doesn't exist, just add it
      evenements = evenements.concat(evenementToAdd)
    }
    this._setEvenements(evenements)
  }

  updateEvenementFilter(evenement_id: string, filter: MessageFilter): Observable<MessageFilter> {
    let evenementToFilter = this.getEvenements().filter(evenement => evenement.uuid === evenement_id)
    evenementToFilter[0].filter = filter
    this.addOrUpdateEvenement(evenementToFilter[0])
    return of(filter)
  }

  setMessages(evenement_id: string, messages: Message[]): void {
    let events = this.getEvenements()
    events.map(event => {
      if (event.uuid === evenement_id) {
        event.messages = messages
      }
      return event
    })
    this._setEvenements(events)
  }

  checkStatus(event: Evenement): EvenementStatus {
    if (event.ended_at) {
      return EvenementStatus.over;
    }
    return new Date(event.started_at) < new Date() ? EvenementStatus.ongoing : EvenementStatus.tobegoing
  }

  getEvenementLocationPolygon(location_id: string): Observable<Location> {
    return this.http.get<any>(`${environment.backendUrl}/locations/${location_id}`)
      .pipe(
        pluck(HTTP_DATA),
        catchError(this.handleError.bind(this))
      )
  }

  mapEvenement(event: Evenement): Evenement {
    return {
      uuid: event.uuid,
      title: event.title,
      description: event.description,
      created_at: event.created_at,
      closed: event.closed,
      started_at: new Date(event.started_at + 'Z'),
      ended_at: event.ended_at,
      user_roles: event.user_roles,
      location_id: event.location_id,
      messages: [],
      creator: {
        position: {
          group: {
            label: event.creator.position.group.label
          }
        }
      },
      filter: {
        etablissement: '',
        auteur: '',
        type: '',
        fromDatetime: '',
        toDatetime: '',
      },
      status: this.checkStatus(event)
    }
  }
  getEvenementsByHTTP(): Observable<Evenement[]> {
    return this.http.get<EvenementsHTTP>(`${environment.backendUrl}/users/me/events`)
      .pipe(
        map(
          response => {
            const evenementsList = response.data.map((event: Evenement) => {
              return this.mapEvenement(event)
            });
            this._setEvenements(evenementsList);
            return evenementsList;
          }
        ),
        catchError(this.handleError.bind(this))
      )
  }
  getSelectedEvenementsParticipants(): Participant[] {
    return this.selectedEvenementParticipants.getValue();
  }
  httpGetEvenementById(uuid: string): Observable<Evenement> {
    return this.http.get<any>(`${this.evenementsUrl}/${uuid}`, this.httpOptions)
      .pipe(
        map(response => {
          let event: Evenement = response.data as Evenement
          event.filter = {
            etablissement: '',
            auteur: '',
            type: '',
            fromDatetime: '',
            toDatetime: '',
          } 
          this.addOrUpdateEvenement(event)
          return event
        }),
        catchError(this.handleError.bind(this))
      )
  }
  addParticipantsToEvenement(participant: Participant): void {
    const copyEvent = this.getEvenementByID(this.selectedEvenementUUID.getValue());
    copyEvent.user_roles = copyEvent.user_roles.concat(participant);
    this.addOrUpdateEvenement(copyEvent);
  }
  changeParticipantRole(participant: Participant): void {
    const copyEvent = this.getEvenementByID(this.selectedEvenementUUID.getValue());
    // Replace the right participant by the received one
    const newUserRoles = copyEvent.user_roles.map(user_role => {
      if (user_role.user.uuid === participant.user.uuid) {
        return participant
      } else {
        return user_role
      }
    });
    copyEvent.user_roles = newUserRoles;
    this.addOrUpdateEvenement(copyEvent);
  }
  selectEvenement(event: Evenement): void {
    this.selectedEvenementUUID.next(event.uuid);
    this.selectedEvenementParticipants.next(event.user_roles);
  }
  getSignalementsForEvenement(uuid): Observable<Affaire[]> {
    return this.http.get<any>(`${this.evenementsUrl}/${uuid}/affairs`, this.httpOptions)
      .pipe(
        map(response => {
          return this.affairesService.mapHTTPAffaires(response.data)
        }),
        catchError(this.handleError.bind(this))
      )
  }

  getMainCouranteData(): Observable<any> {
    return this.http.get<any>(
        `${environment.backendUrl}/events/${this.selectedEvenementUUID.getValue()}/export?format=xlsx`,
        { responseType: "arraybuffer" as "json" }
      ).pipe(
      map((file: ArrayBuffer) => {
        return file;
      }),
      catchError(this.handleError.bind(this))
    )
  }

  closeEvenement(uuid: string): Observable<any> {
    return this.http.put<any>(`${environment.backendUrl}/events/${uuid}/close`, {}).pipe(
      catchError(this.handleError.bind(this))
    )
  }

  httpCreateMeeting(): Observable<any> {
    return this.http.post<any>(`${environment.backendUrl}/events/${this.selectedEvenementUUID.getValue()}/meeting`, {
      evenement_id: this.selectedEvenementUUID.getValue()
    }).pipe(
      pluck(HTTP_DATA),
      catchError(this.handleError.bind(this))
    )
  }
  joinMeeting(meetingUUID: string): void {
    this.httpJoinMeeting(meetingUUID).subscribe(res => {
      window.open(res.direct_uri, '_blank')
    })
  }
  httpJoinMeeting(meetingUUID: string): Observable<any> {
    return this.http.get<any>(`${environment.backendUrl}/events/${this.selectedEvenementUUID.getValue()}/meeting/${meetingUUID}/join`).pipe(
      pluck(HTTP_DATA),
      catchError(this.handleError.bind(this))
    )
  }

  handleError(error: HttpErrorResponse) {
    this.toastService.addMessage(error.message, ToastType.ERROR)
    return throwError(error);
  }
}
