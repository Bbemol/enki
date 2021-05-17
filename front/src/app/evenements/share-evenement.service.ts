import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ShareEvenementService {
  sharePanelActive = new BehaviorSubject<boolean>(false);
  
  constructor() { }

  openPanel(): void {
    this.sharePanelActive.next(true);
  }
  closePanel(): void {
    this.sharePanelActive.next(false);
  }
}
