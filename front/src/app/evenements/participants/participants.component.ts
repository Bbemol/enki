import { HttpClient } from '@angular/common/http';
import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, pluck } from 'rxjs/operators';
import { HTTP_DATA } from 'src/app/constants/constants';
import { Participant, User, ToastType } from 'src/app/interfaces';
import { ToastService } from 'src/app/toast/toast.service';
import { ModalComponent } from 'src/app/ui/modal/modal.component';
import { environment } from 'src/environments/environment';
import { EvenementsService } from '../evenements.service';
const ROLES = {
  admin: 'Administrateur',
  view: 'Lecteur',
  edit: 'Éditeur',
};
@Component({
  selector: 'app-participants',
  templateUrl: './participants.component.html',
  styleUrls: ['./participants.component.scss']
})
export class ParticipantsComponent implements OnInit {
  @Input() participants: BehaviorSubject<Participant[]>;
  @Input() selectedParticipant: Participant;
  roles: object;
  @ViewChild(ModalComponent) modal: ModalComponent;
  roleGroup = new FormGroup({
    role: new FormControl('view', Validators.required)
  })

  constructor(
    private evenementsService: EvenementsService,
    private http: HttpClient,
    private toastService: ToastService,
  ) {
    this.roles = ROLES;
    this.roleGroup.controls.role.valueChanges.subscribe((value: string) => {
      this.updateParticipantRole(value).subscribe((res: User) => {
        this.evenementsService.changeParticipantRole({
          user: res,
          type: value
        });
      });
    });
  }
  updateParticipantRole(value: string): Observable<User> {
    return this.http.put<any>(
      `${environment.backendUrl}/events/${this.evenementsService.selectedEvenementUUID.getValue()}/invite/${this.selectedParticipant.user.uuid}?role_type=${value}`, {}
      ).pipe(
      pluck(HTTP_DATA),
      catchError((error) => {
        this.toastService.addMessage(`Le serveur n'a pas pu changer le rôle de l'utilisateur ${this.selectedParticipant.user.first_name}`, ToastType.ERROR);
        return throwError(error);
      })
    )
  }
  showEditParticipantRights(participant): void {
    this.selectedParticipant = participant
    this.roleGroup.controls.role.setValue(participant.type)
    this.modal.open()
  }
  removeSelectedParticipant(closed: boolean): void {
    if (closed) {
      this.selectedParticipant = null;
    }
  }

  ngOnInit(): void {
  }

  mapUserRoleToLabel(type: string): string {
    return type === 'creator' ? 'Créateur' : ROLES[type];
  }

}
