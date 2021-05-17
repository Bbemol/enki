import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { InvitationComponent } from './invitation/invitation.component';
import { AccountComponent } from './account.component';
import { ReactiveFormsModule } from '@angular/forms';
import { SearchEtablissementComponent } from '../search-etablissement/search-etablissement.component';
import { UserInfoGuard } from '../guards/user-info.guard';
import { DirectivesModule } from '../directives.module';

const routes : Routes = [
  {
    path: 'account',
    component: AccountComponent,
    canActivate: [ UserInfoGuard ],
    children: [
      {
        path: '',
        redirectTo: 'invitation',
        pathMatch: 'full'
      },
      {
        path: 'invitation',
        component: InvitationComponent,
        children: [
          {
            path: 'searchetablissement',
            component: SearchEtablissementComponent
          }
        ]
      }
    ]
  }
]

@NgModule({
  declarations: [
    AccountComponent,
    InvitationComponent
  ],
  imports: [
    CommonModule,
    DirectivesModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes),
    
  ]
})
export class AccountModule { }
