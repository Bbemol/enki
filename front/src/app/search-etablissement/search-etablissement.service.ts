import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';
import { Group } from 'src/app/interfaces';
import { GROUP_INIT } from '../constants/group_init';

@Injectable({
  providedIn: 'root'
})
export class SearchEtablissementService {

  selectedEtablissement = new BehaviorSubject<Group>(GROUP_INIT);
  constructor() {}

  setSelectedEtablissement(etablissement: Group): void {
    this.selectedEtablissement.next(etablissement)
  }

  resetSelectedEtablissement(): void {
    this.selectedEtablissement.next(GROUP_INIT);
  }
}
