import { Component, OnInit } from '@angular/core';
import { Observable, of } from 'rxjs';
import { Intervention, InterventionsService } from '../interventions.service'
import { ActivatedRoute } from '@angular/router';
import { EvenementsService } from 'src/app/evenements/evenements.service';
import { FormControl, FormGroup } from '@angular/forms';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { tap } from 'rxjs/operators';

@Component({
  selector: 'fronts-detail-intervention',
  templateUrl: './detail-intervention.component.html',
  styleUrls: ['./detail-intervention.component.scss']
})
export class DetailInterventionComponent implements OnInit {
  intervention;
  fetchedIntervention;
  uuid;
  evenementsList;
  httpOptions;
  evenementsUrl: string;
  evenementGroup = new FormGroup({
    evenement: new FormControl({value:'', disabled: false})
  });
  constructor(
    private interventionsService: InterventionsService,
    private route: ActivatedRoute,
    private evenementsService: EvenementsService,
    private http: HttpClient
    ) {
      this.evenementsService.getEvenements().subscribe((evenements) => {
        this.evenementsList = evenements
      })
      this.httpOptions = {
        headers: new HttpHeaders({
          'Content-Type':  'application/json'
        })
      }
      this.evenementsUrl = `${environment.backendUrl}/events`
    }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.uuid = params['uuid'];
      if (this.interventionsService.getInterventionFromMemory(this.uuid)) {
        this.intervention = this.interventionsService.getInterventionFromMemory(this.uuid)
        this.fetchedIntervention = true
      } else {
        this.interventionsService.httpGetIntervention(this.uuid).subscribe((intervention) => {
          this.intervention = intervention
          this.fetchedIntervention = true;
        });
      }

    });
  }
  getIntervention(): Observable<Intervention> {
    return of(this.intervention)
  }
  attachEvenementToSignalement(): void {
    this.httpFormSubmit().subscribe(() => {
      this.evenementGroup.controls.evenement.disable()
    })
  }
  modifySelectedEvenement(): void {
    this.evenementGroup.controls.evenement.enable()
  }
  httpFormSubmit(): Observable<any> {
    return this.http.put(`${this.evenementsUrl}/${this.evenementGroup.value.evenement}/affairs/${this.uuid}`, this.httpOptions)
      .pipe(
        tap(() => {
          // change current intervention "evenementID"
          this.interventionsService.interventions = this.interventionsService.interventions.map((intervention) => {
            if (intervention.uuid === this.uuid) {
              intervention.evenementID = this.evenementGroup.value.evenement
            }
            return intervention
          })
        })
      )
  }



}
