import { Location } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { Affaire, Evenement, ToastType } from 'src/app/interfaces';
import { AffairesService } from '../affaires.service';
import { ActivatedRoute, Router } from '@angular/router';
import { EvenementsService } from 'src/app/evenements/evenements.service';
import { FormControl, FormGroup } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { catchError, tap } from 'rxjs/operators';
import { HistoryUrlService } from '../../history-url.service';
import { ToastService } from 'src/app/toast/toast.service';

@Component({
  selector: 'fronts-detail-affaire',
  templateUrl: './detail-affaire.component.html',
  styleUrls: ['./detail-affaire.component.scss']
})
export class DetailAffaireComponent implements OnInit {
  affaire: Affaire;
  fetchedAffaire: boolean;
  uuid: string;
  evenementsList: Evenement[];
  evenementsUrl: string;
  previousLinkLabel: string;
  readonly CREATE_EVENT_VALUE: string;
  evenementGroup = new FormGroup({
    evenement: new FormControl({value:'', disabled: false})
  });
  selectedEvenementTitle: string;
  constructor(
    private affairesService: AffairesService,
    private route: ActivatedRoute,
    private historyUrl: HistoryUrlService,
    private evenementsService: EvenementsService,
    private http: HttpClient,
    private _location: Location,
    private router: Router,
    private toastService: ToastService,
    ) {
      this.CREATE_EVENT_VALUE = 'create';
      this.previousLinkLabel = this.historyUrl.getPreviousLabel()

      this.evenementsList = [];
      this.evenementsUrl = `${environment.backendUrl}/events`;
    }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.uuid = params['uuid'];
      if (this.affairesService.getAffaireByID(this.uuid)) {
        this.affaire = this.affairesService.getAffaireByID(this.uuid)
        this.getEvenements();
        this.fetchedAffaire = true
      } else {
        this.affairesService.httpGetAllAffaires().subscribe(() => {
          this.affaire = this.affairesService.getAffaireByID(this.uuid)
          this.getEvenements();
          this.fetchedAffaire = true;
        });
      }

    });
  }
  ngAfterViewInit(): void {
    document.querySelector('.base').scroll(0,0)
    document.querySelector('main').scroll(0,0)
  }
  getEvenements(): void {
    this.evenementsService.getEvenementsByHTTP().subscribe((evenements) => {
      this.evenementsList = evenements;
      if (this.affaire.evenement_id) {
        this.evenementGroup.controls.evenement.setValue(this.affaire.evenement_id);
        this.selectedEvenementTitle = this.evenementsService.getEvenementByID(this.affaire.evenement_id).title;
      } else {
        this.evenementGroup.controls.evenement.setValue('');
      }
    })
  }
  attachEvenementToAffaire(): void {
    if (this.evenementGroup.controls.evenement.value === this.CREATE_EVENT_VALUE) {
      this.router.navigate(['./create-evenement'], { queryParams: { affaireUUID: this.uuid }, relativeTo: this.route});
      return;
    }
    this.affairesService.attachEvenementToAffaire(this.evenementGroup.value.evenement, this.uuid).subscribe(() => {
      this.selectedEvenementTitle = this.evenementsService.getEvenementByID(this.evenementGroup.controls.evenement.value).title;
    })
  }
  detachEvenementToAffaire(): void {
    this.affairesService.detachEvenementToAffaire(this.evenementGroup.value.evenement, this.uuid).subscribe()
  }
  goBack(): void {
    this._location.back()
  }
}
