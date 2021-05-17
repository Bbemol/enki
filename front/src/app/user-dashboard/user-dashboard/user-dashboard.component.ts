import { Component, OnInit } from '@angular/core';
import { User, Affaire } from 'src/app/interfaces';
import { AffairesService } from '../../affaires/affaires.service';
import { UserService } from '../../user/user.service'
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';
import { DEPARTEMENTS } from './departements';

@Component({
  selector: 'app-user-dashboard',
  templateUrl: './user-dashboard.component.html',
  styleUrls: [
    './user-dashboard.component.scss'
  ]
})
export class UserDashboardComponent implements OnInit {

  affaires: Affaire[];
  user: User;
  meteoIframeLink: SafeResourceUrl;

  constructor(
    private affairesService: AffairesService,
    private userService: UserService,
    private sanitizer: DomSanitizer,
    ) {
    this.affaires = [];
    this.affairesService.httpGetAllAffaires().subscribe((affaires) => {
      this.affaires = affaires;
    });
    this.user = this.userService.user;
    // postal code length is minimum 5
    if (this.user.location_id.length > 3) {
      this.meteoIframeLink = this.sanitizer.bypassSecurityTrustResourceUrl(`https://meteofrance.com/widget/prevision/${this.user.location_id}0##034EA2`);
    } else {
      const currentDep = DEPARTEMENTS.find(departement => {
        return departement.DEP.toString() === this.user.location_id;
      });
      const chefLieu = currentDep.CHEFLIEU;
      this.meteoIframeLink = this.sanitizer.bypassSecurityTrustResourceUrl(`https://meteofrance.com/widget/prevision/${chefLieu}0##034EA2`);
    }
  }

  ngOnInit(): void {
    
  }

  ngAfterViewInit(): void {
    document.querySelector('.base').scroll(0,0)
  }

}
