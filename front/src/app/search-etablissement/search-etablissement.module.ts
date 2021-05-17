import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchEtablissementComponent } from './search-etablissement.component';
import { SearchEtablissementService } from './search-etablissement.service';
import { ReactiveFormsModule } from '@angular/forms';
import { RouterModule, Routes } from '@angular/router';
import { DirectivesModule } from '../directives.module';
import { PipesModule } from '../pipes.module';

const routes: Routes = [
  {
    path: 'search-etablissement',
    component: SearchEtablissementComponent
  }
]

@NgModule({
  declarations: [SearchEtablissementComponent],
  providers: [
    SearchEtablissementService
  ],
  imports: [
    ReactiveFormsModule,
    DirectivesModule,
    PipesModule,
    CommonModule,
    RouterModule.forChild(routes)
  ]
})
export class SearchEtablissementModule { }
