import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Participant, Evenement, ToastType } from 'src/app/interfaces';
import { EvenementsService } from '../evenements.service';
import { BehaviorSubject, Observable, Subscription, throwError } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { catchError } from 'rxjs/operators';
import { environment } from 'src/environments/environment';
import { ToastService } from 'src/app/toast/toast.service';
import { ShareEvenementService } from '../share-evenement.service';

@Component({
  selector: 'app-share-evenement',
  templateUrl: './share-evenement.component.html',
  styleUrls: ['./share-evenement.component.scss','../detail-evenement/detail-evenement.component.scss'],
})
export class ShareEvenementComponent implements OnInit {

  participants = new BehaviorSubject<Participant[]>([]);

  meetingUUID: string;
  evenementSubscriber: Subscription;
  @Input() isPanel: boolean;

  selectedParticipant: Participant;


  constructor(
    private router: Router,
    private activatedRoute: ActivatedRoute,
    public evenementsService: EvenementsService,
    private http: HttpClient,
    private toastService: ToastService,
    private shareEvenementService: ShareEvenementService,
    ) {
    this.selectedParticipant = null;
    this.meetingUUID = null;

    this.evenementSubscriber = this.evenementsService._evenements.subscribe((events) => {
      const currentEvents: Evenement[] = events.filter(event => event.uuid === this.evenementsService.selectedEvenementUUID.getValue())
      this.participants.next(currentEvents[0].user_roles)
    })
    const event = this.evenementsService.getEvenementByID(this.evenementsService.selectedEvenementUUID.getValue())
    this.participants.next(event.user_roles)

    /* this.getMeetingData().subscribe(res => {
      this.meetingUUID = res.data[0].uuid
    }) */

  }

  getMeetingData(): Observable<any> {
    return this.http.get<any>(
      `${environment.backendUrl}/events/${this.evenementsService.selectedEvenementUUID.getValue()}/meeting`
      ).pipe(
        catchError((error) => {
          this.toastService.addMessage(`Impossible de récupérer le salon vidéo en cours`, ToastType.ERROR);
          return throwError(error);
        })
      )
  }

  ngOnInit(): void {
  }

  goToSearchUser(): void {
    this.router.navigate(['./searchuser'], {relativeTo: this.activatedRoute})
  }

  createMeeting(): void {
    this.evenementsService.httpCreateMeeting().subscribe(res => {
      this.meetingUUID = res.uuid
      this.joinMeeting();
    })
  }
  joinMeeting(): void {
    this.evenementsService.httpJoinMeeting(this.meetingUUID).subscribe(
      res => {
        window.open(res.direct_uri, '_blank')
      }
    )
  }

  closePanel(): void {
    this.shareEvenementService.closePanel();
  }

  ngOnDestroy(): void {
    this.evenementSubscriber.unsubscribe();
  }


  onActivate(): void {
    document.querySelector('.base').scroll(0,0)
  }

}
