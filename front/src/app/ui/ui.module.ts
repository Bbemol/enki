import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SvgDefinitionsComponent } from './svg-definitions/svg-definitions.component';
import { SmallHeadingComponent } from './small-heading/small-heading.component';
import { RouterModule } from '@angular/router';
import { ModalComponent } from './modal/modal.component';
import { MenuComponent } from './menu/menu.component';



@NgModule({
  declarations: [
    SvgDefinitionsComponent,
    SmallHeadingComponent,
    ModalComponent,
    MenuComponent,
  ],
  exports: [
    SvgDefinitionsComponent,
    SmallHeadingComponent,
    MenuComponent,
    ModalComponent
  ],
  imports: [
    CommonModule,
    RouterModule
  ]
})
export class UiModule { }
