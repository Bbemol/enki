import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FirstStepComponent } from './register/first-step/first-step.component'
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { RegisterComponent } from './register/register.component';
import { RegisterService } from './register.service';
import { UserInfoGuard } from '../guards/user-info.guard';
import { SearchEtablissementComponent } from '../search-etablissement/search-etablissement.component';
import { DirectivesModule } from '../directives.module';
// import { AuthGuard } from '../app-auth-guard.service';

const routes : Routes = [
  {
    path: 'register',
    component: RegisterComponent,
    // canActivate: [ AuthGuard ],
    canActivate: [ UserInfoGuard ],
    children: [
      {
        path: '',
        redirectTo: 'step1',
        pathMatch: 'full',
      },
      {
        path: 'step1',
        component: FirstStepComponent,
        children: [
          {
            path: 'searchlocation',
            component: SearchEtablissementComponent
          }
        ]
      },
    ]
  }
]

@NgModule({
  declarations: [
    FirstStepComponent,
    RegisterComponent
  ],
  providers: [ RegisterService ],
  imports: [
    DirectivesModule,
    CommonModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes)

  ]
})
export class RegistrationModule { }

