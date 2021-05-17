import { Component } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';
import { environment } from '../environments/environment';
import { UserService } from './user/user.service';
import { Title } from '@angular/platform-browser';
import { MobilePrototypeService } from './mobile-prototype/mobile-prototype.service';
import { BehaviorSubject } from 'rxjs';
import { NavigationStart, Router } from '@angular/router';
import { filter } from 'rxjs/operators';
import { HistoryUrlService } from './history-url.service';
import { ToastService } from './toast/toast.service';
import { FormControl } from '@angular/forms';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'enki';
  affaire;
  fetchedAffaire: boolean;
  token;
  environment;
  user;
  model = new FormControl();
  onBoardingEnabled: boolean;
  showOnboarding = new BehaviorSubject<boolean>(true);
  previousUrl: string;
  currentUrl: string;

  constructor(
    private keycloakService: KeycloakService,
    public userService: UserService,
    private titleService: Title,
    public mobilePrototype: MobilePrototypeService,
    private router: Router,
    private historyUrl: HistoryUrlService,
    private toastService: ToastService,
    ) {
      this.router.events.pipe(filter(event => event instanceof NavigationStart)).subscribe((event: NavigationStart) => {
        this.historyUrl.setPreviousUrl(this.currentUrl)
        this.currentUrl = event.url
      })
      this.titleService.setTitle('Gestion de crise | ENKI')
      this.environment = environment;
      if (environment.auth) {
        this.keycloakService.getToken().then((res) => {
          this.token = res;
          window.localStorage.setItem('token', res);
        })
      }
      this.onBoardingEnabled = false;
      if (this.onBoardingEnabled) {
        this.showOnboarding.next(window.localStorage.getItem('showOnboarding') === 'true' || window.localStorage.getItem('showOnboarding') === null ? true : false);
      } else {
        this.showOnboarding.next(false);
      }
      this.fetchedAffaire = false;

  }
  // tslint:disable-next-line:use-lifecycle-interface
  ngOnInit(): void {
    console.log(`---
Bienvenue sur 🅴🅽🅺🅸 !
Un petit 🅱🅱🆃🅴🅰 ?
---
`)
  }

  onActivate(): void {
    window.scroll(0, 0);
  }

  hideOnboarding(): void {
    window.localStorage.setItem('showOnboarding', 'false')
    this.showOnboarding.next(false)
  }

}
