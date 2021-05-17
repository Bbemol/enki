import { Injectable } from '@angular/core';
import { Observable, of, throwError } from 'rxjs';
import { Contact, ToastType } from 'src/app/interfaces';
import { catchError, map, tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { ToastService } from '../toast/toast.service';

@Injectable({
  providedIn: 'root'
})
export class AnnuaireService {
  contacts: Contact[] = [];
  annuaire: Contact[] = [];

  constructor(
    private http: HttpClient,
    private toastService: ToastService
  ) { }

  // GET /annuaire/search?q=queryString
  searchInAnnuaire(query: string): Observable<Contact[]> {
    return this.http.get<any>(`${environment.backendUrl}/contacts?query=${query}`)
      .pipe(
        map(contacts => {
          this.annuaire = contacts.data
          return contacts.data
        }),
        catchError(this.handleError.bind(this))
      )
  }
  // POST /annuaire/add
  addContactToAnnuaire(contact: Contact): Observable<Contact> {
    return this.http.post<any>(`${environment.backendUrl}/contacts`, contact)
      .pipe(
        tap(contact => {
          this.annuaire = this.annuaire.concat(contact)
        }),
        catchError(this.handleError.bind(this))
      )
  }
  // GET /annuaire/{uuid}
  getContactDetails(contactId: string): Observable<Contact> {
    return this.http.get<any>(`${environment.backendUrl}/contacts/${contactId}`)
      .pipe(
        map(contact => {
          return contact.data
        }),
        catchError(this.handleError.bind(this))
      )
  }
  // PUT /annuaire/{uuid}
  updateContactDetails(contact: Contact): Observable<Contact> {
    return of(contact)
  }
  // DELETE /annuaire/{uuid}
  removeContactFromAnnuaire(contactId: string): Observable<string> {
    return of(contactId)
  }

  handleError(error: HttpErrorResponse) {
      this.toastService.addMessage(error.message, ToastType.ERROR)
      return throwError(error);
  }

}
