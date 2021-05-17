import { Injectable } from '@angular/core';
import { BehaviorSubject, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MobilePrototypeService {
  checked = new BehaviorSubject<boolean>(false);
  constructor() {}

  setChecked(isChecked: boolean): void {
    this.checked.next(isChecked);
  }

  getCheckedClass(): string {
    return this.checked.getValue() ? 'prototype' : ''
  }
}
