import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AuthGuard } from './app-auth-guard.service';
import { UserInfoGuard } from './guards/user-info.guard';
import { ListeAffairesComponent } from './affaires/liste-affaires/liste-affaires.component';
import { UserDashboardComponent } from './user-dashboard/user-dashboard/user-dashboard.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { EvenementsModule } from './evenements/evenements.module';
import { AnnuaireModule } from './annuaire/annuaire.module';
import { RegistrationModule } from './registration/registration.module';
import { DirectivesModule } from './directives.module';

const routes: Routes = [
  {
    path: '',
    canActivate: [ UserInfoGuard ],
    children: [
      {
        path: 'dashboard',
        component: UserDashboardComponent,
      },
      {
        path: 'affaires',
        component: ListeAffairesComponent
      },
    ]
  },
  { path: '**', component: PageNotFoundComponent }

];

@NgModule({
  imports: [
    RouterModule.forRoot(routes, { scrollOffset: [0, 0], scrollPositionRestoration: 'enabled', relativeLinkResolution: 'legacy' }),
    DirectivesModule,
    EvenementsModule,
    AnnuaireModule,
    RegistrationModule,
  ],
  exports: [ RouterModule ],
  providers: [ AuthGuard ]
})
export class AppRoutingModule { }
