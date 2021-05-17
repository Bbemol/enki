import { Component, OnInit } from '@angular/core';
import { KeycloakService } from 'keycloak-angular';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { UserService } from 'src/app/user/user.service';
import { MenuService } from '../menu/menu.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss']
})
export class HeaderComponent implements OnInit {

  menuActive: boolean;

  constructor(
    public userService: UserService,
    public mobilePrototype: MobilePrototypeService,
    private menuService: MenuService,
    ) {
      this.menuService.menuActive.subscribe((value: boolean) => {
        this.menuActive = value;
      })
  }

  ngOnInit(): void {
  }

  closeMenu(): void {
    this.menuService.close();
  }

  openCloseMenu(): void {
    this.menuService.openCloseMenu();
  }

}
