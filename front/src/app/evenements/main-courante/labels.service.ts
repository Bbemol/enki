import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { ToastType } from 'src/app/interfaces';
import { ToastService } from 'src/app/toast/toast.service';
import { environment } from 'src/environments/environment';

export interface Label {
  title: string;
  uuid: string;
}

@Injectable({
  providedIn: 'root'
})
export class LabelsService {
  labels: Array<Label>;
  selectedLabels: Array<Label>;
  labelUrl: string;
  httpHeaders: object;
  constructor(
    private http: HttpClient,
    private toastService: ToastService,
  ) {
    this.labelUrl = `${environment.backendUrl}/tags`
    this.labels = []
    this.selectedLabels = []
    this.httpHeaders = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json'
      })
    }
  }

  addLabel(title): Observable<Label> {
    let tag = {
      "title": title
    }
    return this.http.post<any>(this.labelUrl, tag, this.httpHeaders)
      .pipe(
        map(label => label.data),
        catchError((error) => {
          this.toastService.addMessage(`Impossible d'ajouter ce label`, ToastType.ERROR);
          return throwError(error);
        })
      )
  }
  getLabels(): Observable<Label[]> {
    return this.http.get<any>(this.labelUrl)
      .pipe(
        map(labels => {
          return labels.data
        }),
        catchError((error) => {
          this.toastService.addMessage(`Impossible de récupérer la liste des labels`, ToastType.ERROR);
          return throwError(error);
        })
      )
  }
}
