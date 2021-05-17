import { BrowserModule } from '@angular/platform-browser';
import { NgModule, APP_INITIALIZER } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { KeycloakAngularModule, KeycloakService } from 'keycloak-angular';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UiModule } from './ui/ui.module';
import { environment } from '../environments/environment';
import { ListeAffairesComponent } from './affaires/liste-affaires/liste-affaires.component';
import { HeaderComponent } from './ui/header/header.component';

import { SecondStepComponent } from './registration/second-step/second-step.component';

import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { MobilePrototypeComponent } from './mobile-prototype/mobile-prototype.component';
import { ToastContainerComponent } from './toast/toast-container.component';

import { SearchLocationModule } from './search-location/search-location.module';
import { SearchEtablissementModule } from './search-etablissement/search-etablissement.module';
import { AffairesModule } from './affaires/affaires.module';
import { UserDashboardModule } from './user-dashboard/user-dashboard.module';
import { AccountModule } from './account/account.module';
import { EvenementsModule } from './evenements/evenements.module';
import { AnnuaireModule } from './annuaire/annuaire.module';
import { DirectivesModule } from './directives.module';
import { PipesModule } from './pipes.module';

function initializeKeycloak(keycloak: KeycloakService) {
  return () => {
    return environment.auth ? (
    keycloak.init({
      config: {
        "realm": "enki",
        "url": environment.keycloakUrl,
        "clientId": "angular_frontend",
      },
      initOptions: {
        onLoad: 'login-required'
      },
      bearerExcludedUrls: ['minio:9000'],
    })
    ) : true;
  }
}
@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    ListeAffairesComponent,
    SecondStepComponent,
    PageNotFoundComponent,
    MobilePrototypeComponent,
    ToastContainerComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ReactiveFormsModule,
    DirectivesModule,
    PipesModule,
    KeycloakAngularModule,
    UiModule,
    UserDashboardModule,
    AffairesModule,
    SearchLocationModule,
    SearchEtablissementModule,
    AccountModule,
    EvenementsModule,
    AnnuaireModule,
    AppRoutingModule,
  ],
  providers: [{
    provide: APP_INITIALIZER,
    useFactory: initializeKeycloak,
    multi: true,
    deps: [KeycloakService],
  }],
  bootstrap: [AppComponent]
})
export class AppModule { }
