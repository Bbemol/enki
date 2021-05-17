import { Injectable } from '@angular/core';
import { InMemoryDbService } from 'angular-in-memory-web-api';
import data from '../../data/interventionsx10.json';

@Injectable({
  providedIn: 'root',
})
export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const affaires = data.affairs;
    return { affaires };
  }
  genId(affaires: any): number {
    return affaires.length > 0 ? Math.max(...affaires.map(inter => inter.id)) + 1 : 11;
  }
}