import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { PREVIOUS_PROPERTIES_MAP } from './previous-properties-map';

@Injectable({
  providedIn: 'root'
})
export class HistoryUrlService {
  private _previousUrl = new BehaviorSubject<string>(null);
  constructor() {}
  getPreviousLabel(): string {
    const previousUrl = this.getPreviousUrl();
    let previousLabel = 'Retour';
    const previousProperty = PREVIOUS_PROPERTIES_MAP.find(previousProperty => {
      if (previousProperty.fullPath) {
        return previousProperty.path === previousUrl
      } else {
        return previousUrl ? previousUrl.includes(previousProperty.path) : null
      }
    });

    return previousProperty && previousProperty.value ? `Retourner ${previousProperty.value}` : previousLabel;
  }
  getPreviousUrl(): string {
    return this._previousUrl.getValue();
  }
  setPreviousUrl(url: string): void {
    this._previousUrl.next(url);
  }
}
