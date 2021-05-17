import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

import { DetailAffaireComponent } from './detail/detail-affaire.component';
import { DirectivesModule } from '../directives.module';
import { PipesModule } from '../pipes.module';
import { UiModule } from '../ui/ui.module';

import { CreateEvenementComponent } from '../evenements/create-evenement/create-evenement.component';
import { SearchLocationComponent } from '../search-location/search-location.component';
import { MapModule } from '../map/map.module';

const routes : Routes = [
  {
    path: 'detail-affaire/:uuid',
    component: DetailAffaireComponent,
    children: [
    ]
  },
  {
    path: 'detail-affaire/:uuid/create-evenement',
    component: CreateEvenementComponent,
    children: [
      {
        path: 'searchlocation',
        component: SearchLocationComponent
      }
    ]
  },
];

@NgModule({
  declarations: [
    DetailAffaireComponent,
  ],
  imports: [
    DirectivesModule,
    PipesModule,
    MapModule,
    UiModule,
    CommonModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes)
  ]
})
export class AffairesModule { }
