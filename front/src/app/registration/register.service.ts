import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, of } from 'rxjs';
import { catchError, pluck } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { HTTP_DATA } from '../constants/constants';
import { ToastType } from 'src/app/interfaces';
import { ToastService } from '../toast/toast.service';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {
  token: string;
  private readonly selectedGroupType = new BehaviorSubject<string>('');

  constructor(
    private http: HttpClient,
    private toastService: ToastService,
  ) {
    this.token = '';
  }
  setGroupType(groupType: string): void {
    this.selectedGroupType.next(groupType)
  }

  getUserTypes(): Observable<[]> {
    return this.http.get<any>(`${environment.backendUrl}/groups/types`)
      .pipe(
        pluck(HTTP_DATA),
        catchError(this.handleError('getUserTypes', []))
      )
  }

  getUserPositions(groupeTypeName: string): Observable<object[]> {
    return this.http.get<any>(`${environment.backendUrl}/groups/positions?groupType=${groupeTypeName}`)
      .pipe(
        pluck(HTTP_DATA),
        catchError(this.handleError('getUserPositions', []))
      )
  }

  private handleError(operation: string, result?: any) {
    return (error: any): Observable<any> => {
      this.toastService.addMessage(`${operation} failed: ${JSON.stringify(error)}`, ToastType.ERROR)
      return of(result)
    }
  }

}
