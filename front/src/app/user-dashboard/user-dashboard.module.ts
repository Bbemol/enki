import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { UserDashboardComponent } from './user-dashboard/user-dashboard.component';
import { RouterModule } from '@angular/router';
import { DirectivesModule } from '../directives.module';

@NgModule({
  declarations: [
    UserDashboardComponent
  ],
  imports: [
    CommonModule,
    DirectivesModule,
    RouterModule
  ],
  exports: [
    UserDashboardComponent,
  ]
})
export class UserDashboardModule {}
