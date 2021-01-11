import { catchError, map, tap } from 'rxjs/operators';
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Message {
  title: string;
  description: string;
  created_at: string;
}


@Injectable({
  providedIn: 'root'
})

export class MessagesService {
  messagesUrl: string;
  messages: Array<Message>;
  
  httpHeaders: object;
  constructor(
    private http: HttpClient,
  ) {
    this.messages = window.sessionStorage.getItem("messages") ? JSON.parse(window.sessionStorage.getItem("messages")) : [];
    this.messagesUrl = 'http://localhost:5000/api/enki/v1/messages'

    this.httpHeaders = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    }
  }

  uuidv4(): string {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }



  addMessage(title, description, selectedLabels) : Observable<Message> {
    let uuid = this.uuidv4()
    let message = {
      "title":title,
      "description": description,
      "uuid": uuid,
      "tags": selectedLabels,
      "evenement_id": "event_id"
    }
    return this.http.post<any>(this.messagesUrl, message, this.httpHeaders)
  }

  getMessages(): Observable<Message[]> {
    return this.http.get<any>(this.messagesUrl)
      .pipe(
        map(messages => {
          return messages.messages
        })
      )
  }

}
