import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { Evenement } from 'src/app/interfaces';
import { ShareEvenementService } from '../share-evenement.service';

@Component({
  selector: 'app-detail-evenement',
  templateUrl: './detail-evenement.component.html',
  styleUrls: ['./detail-evenement.component.scss']
})
export class DetailEvenementComponent implements OnInit {
  uuid: string;
  evenement: Evenement;
  backLabel: string;
  isPanelOpened: boolean;
  constructor(
    private route: ActivatedRoute,
    public mobilePrototype: MobilePrototypeService,
    private router: Router,
    private shareEvenementService: ShareEvenementService,
    ) {
      this.isPanelOpened = false;
      this.shareEvenementService.sharePanelActive.subscribe(value => {
        this.isPanelOpened = value;
      })
  }

  ngOnInit(): void {
    this.route.data.subscribe((data: { event: Evenement }) => {
      this.evenement = data.event;
      this.uuid = data.event.uuid;
    });
  }
  goBack(): void {
    this.router.navigate(['evenements'])
  }

  onActivate(): void {
    document.querySelector('.base').scroll(0,0)
  }

}
