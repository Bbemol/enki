import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Routes, RouterModule } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';

import { AuthGuard } from '../app-auth-guard.service';
import { CreateEvenementComponent } from './create-evenement/create-evenement.component';
import { DetailEvenementComponent } from './detail-evenement/detail-evenement.component';
import { SummaryEvenementComponent } from './summary-evenement/summary-evenement.component';
import { MainCouranteComponent } from './main-courante/main-courante.component';
import { AddMessageComponent } from './main-courante/add-message/add-message.component';
import { AddLabelComponent } from './main-courante/add-label/add-label.component';

import { FilterLabelsPipe } from './main-courante/add-label/filter-labels.pipe';
import { FilterMessagesPipe } from './main-courante/filter-messages.pipe';

import { DetailMessageComponent } from './main-courante/detail-message/detail-message.component';
import { EvenementDetailResolverService } from './evenement-detail-resolver.service';
import { ListeMainCouranteComponent } from './main-courante/liste-main-courante/liste-main-courante.component';
import { MessagesService } from './main-courante/messages.service';
import { UiModule } from '../ui/ui.module';
import { UserInfoGuard } from '../guards/user-info.guard';
import { ShareEvenementComponent } from './share-evenement/share-evenement.component';
import { SearchUserComponent } from './share-evenement/search-user/search-user.component';
import { FilterMessagesComponent } from './main-courante/filter-messages/filter-messages.component';
import { SearchLocationComponent } from '../search-location/search-location.component';
import { DirectivesModule } from '../directives.module';
import { CanDeactivateGuard } from '../guards/can-deactivate.guard';
import { PipesModule } from '../pipes.module';
import { ListeEvenementsComponent } from './liste-evenements/liste-evenements.component';
import { TabbarComponent } from './tabbar/tabbar.component';
import { ParticipantsComponent } from './participants/participants.component';
import { ShareTabComponent } from './share-tab/share-tab.component';


const routes : Routes = [
  {
    path: '',
    canActivate: [ UserInfoGuard ],
    children: [
      {
        path: '',
        redirectTo: '/dashboard',
        pathMatch: 'full'
      },
      {
        path: 'evenements',
        component: ListeEvenementsComponent
      },
      {
        path: 'evenements/create',
        canActivate: [ AuthGuard ],
        component: CreateEvenementComponent,
        children: [
          {
            path: 'searchlocation',
            component: SearchLocationComponent
          }
        ]
      },
      {
        path: 'evenements/:uuid',
        canActivate: [AuthGuard],
        component: DetailEvenementComponent,
        resolve: {
          event: EvenementDetailResolverService
        },
        children: [
          {
            path: '',
            redirectTo: 'summary',
            pathMatch: 'full'
          },
          {
            path: 'summary',
            component: SummaryEvenementComponent,
          },
          {
            path: 'maincourante',
            component: MainCouranteComponent,
            children: [
              {
                path: '',
                pathMatch: 'full',
                redirectTo: 'liste',
              },
              {
                path: 'liste',
                component: ListeMainCouranteComponent,
                children: [
                  {
                    path: 'message/:uuid',
                    component: DetailMessageComponent
                  },
                  {
                    path: 'addmessage',
                    component: AddMessageComponent,
                    canDeactivate: [CanDeactivateGuard],
                    children: [
                      {
                        path: 'addlabel',
                        component: AddLabelComponent
                      }
                    ]
                  },
                ]
              },
            ]
          },
          {
            path: 'share',
            component: ShareTabComponent,
            children: [
              {
                path: 'searchuser',
                component: SearchUserComponent,
              }
            ]
          }
        ]
      }
    ]
  }
]

@NgModule({
  declarations: [
    ListeEvenementsComponent,
    CreateEvenementComponent,
    DetailEvenementComponent,
    MainCouranteComponent,
    AddMessageComponent,
    AddLabelComponent,
    FilterLabelsPipe,
    DetailMessageComponent,
    SummaryEvenementComponent,
    ListeMainCouranteComponent,
    ShareEvenementComponent,
    SearchUserComponent,
    FilterMessagesPipe,
    FilterMessagesComponent,
    TabbarComponent,
    ParticipantsComponent,
    ShareTabComponent,
  ],
  providers: [
    MessagesService,
  ],
  imports: [
    DirectivesModule,
    PipesModule,
    UiModule,
    CommonModule,
    ReactiveFormsModule,
    RouterModule.forChild(routes)
  ]
})
export class EvenementsModule { }
