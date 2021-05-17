import { catchError, map } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { BehaviorSubject, Observable, of, throwError } from 'rxjs';
import { environment } from 'src/environments/environment';
import { uuidv4 } from '../../utilities';
import { EvenementsService } from '../evenements.service';
import { Message, ToastType } from 'src/app/interfaces';
import { ToastService } from 'src/app/toast/toast.service';


@Injectable({
  providedIn: 'root'
})

export class MessagesService {
  messagesUrl: string;
  resourcesUrl: string;
  private readonly _messagesSource = new BehaviorSubject<Message[]>([]);
  public messages$: Observable<Message[]>;

  constructor(
    private http: HttpClient,
    private evenementsService: EvenementsService,
    private toastService: ToastService,
    ) {
      this.resourcesUrl = `${environment.backendUrl}/resources`
      this.messagesUrl = `${environment.backendUrl}/messages`
      this.messages$ = this._messagesSource.asObservable()
  }

  getMessages(): Message[] {
    return this._messagesSource.getValue();
  }

  private _setMessages(messages: Message[]): void {
    this._messagesSource.next(messages)
  }

  private addMessages(messages: Message[], evenement_id: string): void {
    messages.map(message => {
      message.evenement_id = evenement_id
    })
    const messagesConcat = [...this.getMessages(), ...messages]
    this._setMessages(messagesConcat)
  }

  private containsEvenementMessages(evenementUUID: string): boolean {
    return this.getMessages().some(message => message.evenement_id === evenementUUID)
  }


  getMessagesByEvenementID(evenementUUID: string): Observable<Message[]> {
    const messages = this.getMessages().filter(message => message.evenement_id === evenementUUID)
    return this.containsEvenementMessages(evenementUUID) ? of(messages) : this.httpGetMessages(evenementUUID)
    // return this.httpGetMessages(evenementUUID)
  }

  httpGetMessages(evenementUUID: string): Observable<Message[]> {
    return this.http.get<any>(`${environment.backendUrl}/events/${evenementUUID}/messages`)
      .pipe(
        map(messages => {
          if (!this.containsEvenementMessages(evenementUUID)) {
            this.addMessages(messages.data, evenementUUID)
          }
          return messages.data
        }),
        catchError((error) => {
          this.toastService.addMessage(`Impossible de récupérer les messages de cet événement`, ToastType.ERROR);
          return throwError(error);
        })
      )
  }

  getMessageByID(messageUUID: string): Observable<Message> {
    const message = this.getMessages().filter(message => message.uuid === messageUUID)
    return message.length > 0 ? of(message[0]) : this.httpGetMessageByID(messageUUID)
  }

  httpGetMessageByID(messageUUID: string): Observable<Message> {
    return this.http.get<any>(`${environment.backendUrl}/events/${this.evenementsService.selectedEvenementUUID.getValue()}/messages/${messageUUID}`)
      .pipe(
        map(response => {
          return response.data
        }),
        catchError((error) => {
          this.toastService.addMessage(`Impossible de récupérer ce message`, ToastType.ERROR);
          return throwError(error);
        })
      )
  }

  httpSubmitMessage(title, description, selectedLabels, event_id, resources, restricted) : Observable<Message> {
    let uuid = uuidv4()
    let message = {
      "title":title,
      "description": description,
      "uuid": uuid,
      "tag_ids": selectedLabels,
      "evenement_id": event_id,
      "resource_ids": resources,
      "restricted_user_group": restricted
    }
    return this.http.post<any>(`${environment.backendUrl}/events/${this.evenementsService.selectedEvenementUUID.getValue()}/messages`, message)
      .pipe(
        map(message => {
          this.addMessages([message.data], event_id)
          return message.data
        }),
        catchError((error) => {
          this.toastService.addMessage(`Impossible de soumettre ce message`, ToastType.ERROR);
          return throwError(error);
        })
      )
  }

  getUrlFileUpload(file: any): Observable<any> {
    let formBody = {
      "content_type": file.type,
      "original_name": file.name
    }
    return this.http.post<any>(`${this.resourcesUrl}`, formBody).pipe(
      catchError((error) => {
        this.toastService.addMessage(`Impossible d'envoyer le fichier sur le serveur`, ToastType.ERROR);
        return throwError(error);
      })
    )
  }

  getUrlFileDownload(uuid: string): Observable<any> {
    return this.http.get<any>(`${this.resourcesUrl}/${uuid}`).pipe(
      catchError((error) => {
        this.toastService.addMessage(`Impossible de récupérer les informations de la pièce jointe`, ToastType.ERROR);
        return throwError(error);
      })
    )
  }
  removeFileFromServer(resourceUUID: string): Observable<any> {
    return this.http.delete<any>(`${this.resourcesUrl}/${resourceUUID}`).pipe(
      catchError((error) => {
        this.toastService.addMessage(`Une erreur est survenue lors de la suppression de la pièce jointe sur le serveur`, ToastType.ERROR);
        return throwError(error);
      })
    )
  }
  putFileOnServer(file, url): Observable<any> {
    const httpHeaders = {
      headers: new HttpHeaders({
        'Content-Type':  file.type
      })
    }
    return this.http.put<any>(url, file, httpHeaders)
      .pipe(
        catchError((error) => {
          if (error.error instanceof ErrorEvent) {
            // A client-side or network error occurred. Handle it accordingly.
            console.error('An error occurred:', error.error.message);
          } else {
            // The backend returned an unsuccessful response code.
            // The response body may contain clues as to what went wrong.
            console.error(
              `Backend returned code ${error.status}, ` +
              `body was: ${error.error}`);
          }
          return throwError(
            'Something really bad happend'
          )
        })
      )
  }


}
