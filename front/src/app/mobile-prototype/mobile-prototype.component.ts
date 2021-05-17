import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MobilePrototypeService } from './mobile-prototype.service';

@Component({
  selector: 'app-mobile-prototype',
  templateUrl: './mobile-prototype.component.html'
})
export class MobilePrototypeComponent implements OnInit {

  checked = new FormControl()
  constructor(
    public prototypeService: MobilePrototypeService
  ) {
    this.checked.setValue(this.prototypeService.checked.getValue())
    this.checked.valueChanges.subscribe(isChecked => {
      this.prototypeService.setChecked(isChecked);
    })
  }

  ngOnInit(): void {
  }

}
