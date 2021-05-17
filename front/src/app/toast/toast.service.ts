import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { Toast, ToastType } from 'src/app/interfaces';
@Injectable({
  providedIn: 'root'
})

export class ToastService {
  
  private readonly _messages = new Subject<Toast>();
  readonly messages$ = this._messages.asObservable();

  constructor() { }

  addMessage(message: string, toastType: ToastType): void {
    this._messages.next({
      message: message,
      type: toastType
    });
  }
  
}
