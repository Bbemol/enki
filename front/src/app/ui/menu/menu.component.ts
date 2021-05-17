import { Component, OnInit } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';
import { MenuService } from './menu.service';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent implements OnInit {
  menuActive: boolean;
  constructor(
    private keycloakService: KeycloakService,
    private menuService: MenuService,
  ) {
    this.menuService.menuActive.subscribe((value: boolean) => {
      this.menuActive = value;
    });
  }

  ngOnInit(): void {
  }
  openCloseMenu(): void {
    this.menuService.openCloseMenu();
  }
  closeMenu(): void {
    this.menuService.close();
  }
  logout(): void {
    this.keycloakService.logout();
  }
}
