import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss']
})
export class ModalComponent implements OnInit {
  isOpened: boolean;
  @Input() title: string;
  @Input() description: string;
  @Output() closed = new EventEmitter<boolean>();

  constructor(
    public mobilePrototype: MobilePrototypeService
  ) {
    this.isOpened = false;
  }

  ngOnInit(): void {
  }

  open(): void {
    this.isOpened = true;
  }

  close(): void {
    this.isOpened = false;
    this.closed.emit(true);
  }

}
