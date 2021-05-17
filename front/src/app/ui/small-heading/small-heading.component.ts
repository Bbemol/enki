import { Location } from '@angular/common';
import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-small-heading',
  template: `
    <div class="small-heading">
      <div class="small-heading--title">
        {{title}}
      </div>
      <div class="small-heading--close" (click)="close()">
        Fermer
        <svg class="icon-close title-icon"><use xlink:href="#icon-close"></use></svg>
      </div>
    </div>
  `,
  styleUrls: ['./small-heading.component.scss']
})
export class SmallHeadingComponent implements OnInit {
  @Input() title: string;
  @Output() closeEvent = new EventEmitter();
  constructor(
  ) { }

  close(): void {
    this.closeEvent.emit();
  }

  ngOnInit(): void {
  }

}
