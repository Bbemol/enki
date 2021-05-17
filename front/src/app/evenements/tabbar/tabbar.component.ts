import { Component, OnInit } from '@angular/core';
import { ShareEvenementService } from '../share-evenement.service';

@Component({
  selector: 'app-tabbar',
  templateUrl: './tabbar.component.html',
  styleUrls: ['./tabbar.component.scss']
})
export class TabbarComponent implements OnInit {

  constructor(
    private shareEvenementService: ShareEvenementService,
  ) { }

  ngOnInit(): void {
  }
  openSharePanel(): void {
    this.shareEvenementService.openPanel();
  }


}
