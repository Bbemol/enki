import { Location } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-small-heading',
  template: `
    <div class="small-heading">
      <div class="small-heading--title">
        {{title}}
      </div>
      <div class="small-heading--close" (click)="goBack()">
        Fermer
        <svg class="icon-close title-icon"><use xlink:href="#icon-close"></use></svg>
      </div>
    </div>
  `,
  styleUrls: ['./small-heading.component.scss']
})
export class SmallHeadingComponent implements OnInit {
  @Input() title: string;
  @Input() backLink: string;
  constructor(
    private _location: Location
  ) { }

  goBack(): void {
    this._location.back();
  }

  ngOnInit(): void {
  }

}
