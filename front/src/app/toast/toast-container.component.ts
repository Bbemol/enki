import { Component, ComponentFactoryResolver, OnInit, ViewChild } from '@angular/core';
import { Subscription } from 'rxjs';
import { ToastDirective } from '../toast.directive';
import { ToastComponent } from './toast.component';
import { ToastService } from './toast.service';

@Component({
  selector: 'app-toast-container',
  template: `
    <div class="toast-container">
      <ng-template toastHost></ng-template>
    </div>
  `,
  styleUrls: ['./toast-container.component.scss']
})
export class ToastContainerComponent implements OnInit {
  
  @ViewChild(ToastDirective, {static: true}) toastHost: ToastDirective;

  constructor(
    private componentFactoryResolver: ComponentFactoryResolver,
    private toastService: ToastService,
    ) {
    }
    
  ngOnInit(): void {
    const viewContainerRef = this.toastHost.viewContainerRef;
    viewContainerRef.clear();
    this.toastService.messages$.subscribe((message) => {
      const componentFactory = this.componentFactoryResolver.resolveComponentFactory(ToastComponent);
      const componentRef = viewContainerRef.createComponent<ToastComponent>(componentFactory);
      const viewRefChild = componentRef.hostView
      componentRef.instance.message = message;
      componentRef.instance.toastID = viewContainerRef.indexOf(viewRefChild);
      const sub: Subscription = componentRef.instance.removeToast.subscribe(toastID => {
        this.toastHost.viewContainerRef.remove(toastID);
      });
      componentRef.onDestroy(()=> { sub.unsubscribe(); console.log("Unsubscribing")});
      setTimeout(() => {
        viewContainerRef.remove();
      }, 5000)
    })
  }

}
