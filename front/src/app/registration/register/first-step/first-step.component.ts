import { Component } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Validators } from '@angular/forms';
import { Observable, of} from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { UserService } from '../../../user/user.service';
import { ActivatedRoute, Router } from '@angular/router';
import { environment } from 'src/environments/environment';
import { RegisterService } from '../../register.service';
import { HTTP_DATA, REGISTER } from 'src/app/constants/constants';
import { catchError, pluck } from 'rxjs/operators';
import { SearchEtablissementService } from 'src/app/search-etablissement/search-etablissement.service';
import { ToastService } from 'src/app/toast/toast.service';
import { ToastType } from 'src/app/interfaces';

@Component({
  selector: 'app-first-step',
  templateUrl: './first-step.component.html',
  styleUrls: ['./first-step.component.scss']
})
export class FirstStepComponent {

  userGroup = new FormGroup({
    firstName: new FormControl('', Validators.required),
    lastName: new FormControl('', Validators.required),
    group: new FormControl('', Validators.required),
    position: new FormControl('', Validators.required),
    etablissement: new FormControl('', Validators.required),
  })
  fonctions: object;
  updateUserUrl: string;
  userTypes: [];
  userPositions: object[];
  structurePreFilled: boolean;
  userGroupPreFilled: boolean;

  constructor(
    private http: HttpClient,
    private router: Router,
    private userService: UserService,
    private registerService: RegisterService,
    private etablissementService: SearchEtablissementService,
    private route: ActivatedRoute,
    private toastService: ToastService,
  ) {
    this.structurePreFilled = false;
    this.userGroupPreFilled = false;

    this.etablissementService.selectedEtablissement.subscribe((etablissement) => {
      this.userGroup.get('etablissement').setValue(etablissement.label)
    })

    this.registerService.getUserTypes().subscribe(response => {
      this.userTypes = response
    })


    this.userGroup.get('group').valueChanges.subscribe(typeName => {
      this.registerService.setGroupType(typeName);
      this.registerService.getUserPositions(typeName).subscribe(positions => {
        this.userPositions = positions
      })
    })
  }

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      if (params['token']) {
        this.validateInvitationToken(params['token']).subscribe(res => {
          this.userGroup.controls.group.setValue(res.group.type.toLowerCase())
          this.userGroupPreFilled = true;
          this.structurePreFilled = true;
          this.registerService.token = params['token'];
          this.etablissementService.selectedEtablissement.next(res.group)
        })
      }

    });
  }

  validateInvitationToken(token: string): Observable<any> {
    return this.http.post(`${environment.backendUrl}/invitation/validate?token=${token}`, {}).pipe(
      pluck(HTTP_DATA),
      catchError(this.handleError('validateInvitationToken'))
    )
  }

  private handleError<T>(operation = 'operation', result?: T) {
    return (error: any): Observable<any> => {

      // TODO: send the error to remote logging infrastructure
      console.error(error); // log to console instead

      // TODO: better job of transforming error for user consumption
      this.toastService.addMessage(`${operation} failed: ${error.message}`, ToastType.ERROR);

      // Let the app keep running by returning an empty result.
      return of(result);
    };
  }

  onSubmit(): void {
    let bodyForm = {
        position_id: this.userGroup.value.position,
        first_name: this.userGroup.value.firstName,
        last_name: this.userGroup.value.lastName,
        group_type: this.userGroup.value.group,
        group_id: this.etablissementService.selectedEtablissement.getValue().uuid
    }
    this.httpSubmitForm(bodyForm).subscribe((response) => {
      this.userService.user.attributes = {
        fonction: this.userGroup.value.fonction
      }
      this.router.navigate(['dashboard'])

    })
  }

  httpSubmitForm(bodyForm): Observable<any> {
    const submitUrl = this.registerService.token ? `${environment.backendUrl}/users?token=${this.registerService.token}` : `${environment.backendUrl}/users`
    return this.http.post<any>(submitUrl, bodyForm).pipe(
      catchError(() => {
        return of([])
      })
    )
  }

  goToSearchLocation() {
    this.router.navigate([`${REGISTER}/step1/searchlocation`], { queryParams: { groupType: this.userGroup.controls.group.value }})
  }

  ngOnDestroy(): void {
    this.etablissementService.resetSelectedEtablissement();
  }
}
