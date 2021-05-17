import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-account',
  template: `
    <router-outlet (activate)="onActivate()"></router-outlet>
  `,
  styles: [
  ]
})
export class AccountComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  onActivate(): void {
    document.querySelector('.base').scroll(0,0)
  }

}
