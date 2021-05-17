import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FocusFormInputDirective } from './focus-form-input.directive';
import { ToastDirective } from './toast.directive';



@NgModule({
  declarations: [
    FocusFormInputDirective,
    ToastDirective,
  ],
  imports: [
    CommonModule
  ],
  exports: [
    FocusFormInputDirective,
    ToastDirective,
  ]
})
export class DirectivesModule { }
