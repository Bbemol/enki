import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MenuService {
  menuActive = new BehaviorSubject<boolean>(false);

  constructor() {
  }
  close() {
    this.menuActive.next(false);
  }

  openCloseMenu() {
    this.menuActive.getValue() ? this.menuActive.next(false) : this.menuActive.next(true);
  }
}
