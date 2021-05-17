import { Component, OnInit } from '@angular/core';
import { Contact } from 'src/app/interfaces';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { UserService } from 'src/app/user/user.service';

@Component({
  selector: 'app-contact-list',
  templateUrl: './contact-list.component.html',
  styleUrls: ['./contact-list.component.scss']
})
export class ContactListComponent implements OnInit {
  contacts: Contact[];
  constructor(
    private userService: UserService,
    public mobilePrototype: MobilePrototypeService
  ) {
    this.contacts = [];
  }

  ngOnInit(): void {
    this.userService.getUserFavoriteContacts().subscribe((res) => {
      this.contacts = this.sort(res);
    })
  }

  sort(contacts: Contact[]): Array<Contact> {
    return contacts.sort(this.compare)
  }
  compare(a, b): any {
    if (a.first_name.toLowerCase() < b.first_name.toLowerCase()) {
      return -1;
    }
    if (a.first_name.toLowerCase() > b.first_name.toLowerCase()) {
      return 1;
    }
    return 0;
  }

  compareIfFirstLetterIsDifferent(contactA, contactB): boolean {
    if (contactA && contactB && contactA.first_name[0] !== contactB.first_name[0]) {
      return true;
    }
    return contactA === undefined;
  }

}
