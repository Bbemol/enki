import { Component, OnInit } from '@angular/core';
import { AffairesService } from '../affaires.service'
import { environment } from '../../../environments/environment';

@Component({
  selector: 'app-liste-affaires',
  templateUrl: './liste-affaires.component.html',
  styleUrls: ['./liste-affaires.component.scss']
})
export class ListeAffairesComponent implements OnInit {
  affaires;
  constructor(
    private affairesService: AffairesService,
  ) {
    this.affaires = [];
    this.affairesService.httpGetAllAffaires().subscribe((affaires) => {
        this.affaires = affaires
    });
  }
  ngOnInit(): void {

  }
  ngAfterViewInit(): void {
    document.querySelector('.base').scroll(0,0)
    document.querySelector('main').scroll(0,0)
  }
}
