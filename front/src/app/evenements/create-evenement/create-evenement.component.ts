import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Observable, throwError } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { EvenementsService } from '../evenements.service';
import { Evenement, EvenementType, ToastType } from 'src/app/interfaces';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { SearchLocationService } from 'src/app/search-location/search-location.service';
import { HTTP_DATA } from 'src/app/constants/constants';
import { catchError, pluck } from 'rxjs/operators';
import { AffairesService } from 'src/app/affaires/affaires.service';
import { ToastService } from 'src/app/toast/toast.service';

@Component({
  selector: 'app-create-evenement',
  templateUrl: './create-evenement.component.html',
  styleUrls: ['./create-evenement.component.scss']
})
export class CreateEvenementComponent implements OnInit {

  evenementGroup = new FormGroup({
    nomEvenement: new FormControl('', Validators.required),
    descriptionEvenement: new FormControl('', Validators.required),
    startDate: new FormControl('', Validators.required),
    startNow: new FormControl(true),
    location: new FormControl('', Validators.required),
    eventType: new FormControl('', Validators.required)
  })

  evenementUrl: string;
  evenement: object;
  httpOptions: object;
  todayDay: Date;
  attachAffaireUUID: string;
  public EvenementTypeEnum = EvenementType;

  constructor(
    private http: HttpClient,
    private evenementsService: EvenementsService,
    private router: Router,
    private searchLocationService: SearchLocationService,
    private affairesService: AffairesService,
    private activatedRoute: ActivatedRoute,
    private toastService: ToastService,
  ) {
    this.attachAffaireUUID = this.activatedRoute.snapshot.queryParams['affaireUUID'];
    this.todayDay = new Date();
    this.evenementUrl = `${environment.backendUrl}/events`
    this.searchLocationService.selectedEtablissement.subscribe(location => {
      this.evenementGroup.controls.location.setValue(location.label)
    })
  }
  close(): void {
    this.router.navigate(['/evenements']);
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    const startDate = !this.evenementGroup.controls.startNow.value ? (new Date(this.evenementGroup.controls.startDate.value)).toISOString() : (new Date()).toISOString()
    let formBody = {
      "creator_id": "my_id",
      "title": this.evenementGroup.value.nomEvenement,
      "description": this.evenementGroup.value.descriptionEvenement,
      "started_at": startDate,
      "location_id": this.searchLocationService.selectedEtablissement.getValue().uuid,
      "type": this.evenementGroup.value.eventType
    }
    this.httpFormSubmit(formBody).subscribe(response => {
      this.evenementsService.addOrUpdateEvenement(response)
      if (this.attachAffaireUUID) {
        this.affairesService.attachEvenementToAffaire(response.uuid, this.attachAffaireUUID).subscribe(() => {
          this.router.navigate([`evenements/${response.uuid}`])
        });
      } else {
        this.router.navigate([`evenements/${response.uuid}`])
      }
    })
  }

  goToSearchLocation(): void {
    this.router.navigate([`searchlocation`], { relativeTo: this.activatedRoute})

  }

  httpFormSubmit(formBody): Observable<Evenement> {
    return this.http.post<any>(this.evenementUrl, formBody).pipe(
      pluck(HTTP_DATA),
      catchError((error) => {
        this.toastService.addMessage(`Impossible de créer l'événement`, ToastType.ERROR);
        return throwError(error);
      })
    )
  }
  ngAfterViewInit(): void {
    document.querySelector('.base').scroll(0,0)
  }
  ngOnDestroy(): void {
    this.searchLocationService.resetSelectedLocation();
  }

}
