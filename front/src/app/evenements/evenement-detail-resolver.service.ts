import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, Resolve, Router, RouterStateSnapshot } from '@angular/router';
import { EMPTY, Observable, of } from 'rxjs';
import { mergeMap, take } from 'rxjs/operators';
import { EvenementsService } from './evenements.service';
import { Evenement } from 'src/app/interfaces';

@Injectable({
  providedIn: 'root'
})
export class EvenementDetailResolverService implements Resolve<Evenement> {

  constructor(
    private router: Router,
    private evenementsService: EvenementsService
  ) { }
  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Evenement> | Observable<never> {
    const id = route.paramMap.get('uuid')
    
    return this.evenementsService.httpGetEvenementById(id).pipe(
      take(1),
      mergeMap(event => {
        if(event) {
          this.evenementsService.selectEvenement(event)
          return of(event)

        } else {
          this.router.navigate(['/dashboard'])
          return EMPTY
        }
      })
    )
    /* this.route.params.subscribe(params => {
      this.uuid = params['uuid'];
      this.evenementsService.getEvenement(this.uuid).subscribe((evenement) => {
        this.fetchedEvenement = true;
        this.evenement = evenement
      });
    }) */
  }
}
