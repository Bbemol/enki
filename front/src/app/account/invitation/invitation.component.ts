import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { RegisterService } from 'src/app/registration/register.service';
import { SearchEtablissementService } from 'src/app/search-etablissement/search-etablissement.service';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-invitation',
  templateUrl: './invitation.component.html',
  styleUrls: ['./invitation.component.scss']
})
export class InvitationComponent implements OnInit {


  invitationGroup = new FormGroup({
    email: new FormControl('', Validators.required),
    phone: new FormControl('', Validators.required),
    group: new FormControl('', Validators.required),
    etablissement: new FormControl('', Validators.required),
  })

  groupTypes: [];

  constructor(
    private registerService: RegisterService,
    private router: Router,
    private etablissementService: SearchEtablissementService,
    private http: HttpClient
  ) {
    this.registerService.getUserTypes().subscribe(response => {
      this.groupTypes = response
    })

    this.etablissementService.selectedEtablissement.subscribe((structure) => {
      this.invitationGroup.get('etablissement').setValue(structure.label)
    })
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    /* 
  {
    "creator_id": "string",
    "email": "user@example.com",
    "expire_at": "2021-03-15T08:28:29.367Z",
    "group_id": "string",
    "group_type": "string",
    "phone_number": "string",
    "uuid": "string",
    "validated_at": "2021-03-15T08:28:29.367Z"
  }
 */
    let bodyForm = {
      email: this.invitationGroup.value.email,
      phone_number: this.invitationGroup.value.phone,
      group_type: this.invitationGroup.value.group,
      group_id: this.etablissementService.selectedEtablissement.getValue().uuid
    }
    this.httpSubmitForm(bodyForm).subscribe((response) => {
      console.log('fill out the form', response)
    })
  }

  httpSubmitForm(body: object): Observable<any> {
    return this.http.post<any>(`${environment.backendUrl}/invitation`, body)
  }

  goToSearchEtablissement(): void {
    this.router.navigate([`account/invitation/searchetablissement`], { queryParams: { groupType: this.invitationGroup.controls.group.value }})
  }

}
