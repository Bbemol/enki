import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Location } from 'src/app/interfaces';
import { LOCATION_INIT } from '../constants/location_init';

@Injectable({
  providedIn: 'root'
})
export class SearchLocationService {

  selectedEtablissement = new BehaviorSubject<Location>(LOCATION_INIT);
  constructor() { }

  setSelectedLocation(location: Location): void {
    this.selectedEtablissement.next(location);
  }
  resetSelectedLocation(): void {
    this.selectedEtablissement.next(LOCATION_INIT);
  }
}
