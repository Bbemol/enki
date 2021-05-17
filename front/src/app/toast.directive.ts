import { Directive, ViewContainerRef } from '@angular/core';

@Directive({
  selector: '[toastHost]'
})
export class ToastDirective {

  constructor(public viewContainerRef: ViewContainerRef) { }

}
