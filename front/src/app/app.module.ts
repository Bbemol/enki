import { BrowserModule } from '@angular/platform-browser';
import { NgModule, APP_INITIALIZER } from '@angular/core';
import { KeycloakAngularModule, KeycloakService } from 'keycloak-angular';

import { AppRoutingModule } from './app-routing.module';
import { HttpClientModule } from '@angular/common/http';
import { AppComponent } from './app.component';
import { MapComponent } from './map/map.component';
import { environment } from '../environments/environment';
import { ListeInterventionsComponent } from './interventions/liste/liste-interventions.component';
import { DetailInterventionComponent } from './interventions/detail/detail-intervention.component';
import { SvgDefinitionsComponent } from './ui/svg-definitions/svg-definitions.component';
import { HeaderComponent } from './ui/header/header.component';

import { HttpClientInMemoryWebApiModule } from 'angular-in-memory-web-api';
import { InMemoryDataService } from './in-memory-data.service';
import { FirstStepComponent } from './registration/first-step/first-step.component';
import { SecondStepComponent } from './registration/second-step/second-step.component';

import { ReactiveFormsModule } from '@angular/forms';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';

import { UserDashboardModule } from './user-dashboard/user-dashboard.module';
import { MainCouranteModule } from './main-courante/main-courante.module';

function initializeKeycloak(keycloak: KeycloakService) {
  return () =>
    keycloak.init({
      config: {
        "realm": "enki",
        "url": "http://localhost:8084/auth/",
        "clientId": "angular_frontend",
      },
      initOptions: {
        onLoad: 'login-required'
      },
    });
}
@NgModule({
  declarations: [
    AppComponent,
    MapComponent,
    ListeInterventionsComponent,
    DetailInterventionComponent,
    SvgDefinitionsComponent,
    HeaderComponent,
    FirstStepComponent,
    SecondStepComponent,
    PageNotFoundComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    ReactiveFormsModule,
    // The HttpClientInMemoryWebApiModule module intercepts HTTP requests
    // and returns simulated server responses.
    // Remove it when a real server is ready to receive requests.
    environment.HTTPClientInMemory ? HttpClientInMemoryWebApiModule.forRoot(
      InMemoryDataService, { dataEncapsulation: false }
    ) : [],
    KeycloakAngularModule,
    AppRoutingModule,
    UserDashboardModule,
    MainCouranteModule
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
