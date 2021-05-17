import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { Contact, ToastType, User } from 'src/app/interfaces';
import { ToastService } from '../toast/toast.service';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  user: User;
  userExist: boolean;

  constructor(
    private http: HttpClient,
    private toastService: ToastService,
  ) {
    this.user = {
      attributes: {
        fonction: ''
      },
      location: '',
      location_id: '',
      contacts: [],
      uuid: ''
    };

  }

  getUserInfo(): Observable<any> {
    return this.http.get(`${environment.backendUrl}/users/me`).pipe(
      catchError((error) => {
        if (error.status !== 404) {
          this.toastService.addMessage(`Impossible de récupérer les données utilisateurs`, ToastType.ERROR);
        }
        return throwError(error)
      })
    )
  }

  // GET /user/{uuid}/favoriteContacts
  getUserFavoriteContacts(): Observable<Contact[]> {
    return this.http.get<any>(`${environment.backendUrl}/users/me/contact/favorites`)
      .pipe(
        map(contacts => {
          this.user.contacts = contacts.data
          return contacts.data
        }),
        catchError((error) => {
          this.toastService.addMessage(`Impossible de récupérer les contacts favoris de l'utilisateur`, ToastType.ERROR);
          return throwError(error)
        })
      )
  }
  isUserFav(contactId: string): boolean {
    return this.user.contacts.some(contact => contact.uuid === contactId);
  }
  // PUT /user/me/favoriteContacts/{uuid}
  addContactToUserFavs(contactId: string): Observable<Contact[]> {
    return this.http.put<any>(`${environment.backendUrl}/users/me/contact/favorites/${contactId}`, '')
      .pipe(
        tap(response => {
          this.user.contacts = response.data;
        }),
        catchError((error) => {
          this.toastService.addMessage(`Impossible d'ajouter le contact aux favoris`, ToastType.ERROR);
          return throwError(error)
        })
      );
  }
  // DELETE /user/{uuid}/favoriteContacts/{uuid}
  removeContactFromUserFavs(contactId: string): Observable<Contact[]> {
    return this.http.delete<any>(`${environment.backendUrl}/users/me/contact/favorites/${contactId}`)
      .pipe(
        tap(response => {
          this.user.contacts = response.data
        }),
        catchError((error) => {
          this.toastService.addMessage(`Impossible de supprimer le contact aux favoris`, ToastType.ERROR);
          return throwError(error)
        })
      )
  }

  userIsValid(): boolean {
    return Object.keys(this.user).length > 0 && this.user.location !== '' && this.user.attributes.fonction !== '';
  }

}
