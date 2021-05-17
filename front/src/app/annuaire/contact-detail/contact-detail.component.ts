import { Location } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HistoryUrlService } from 'src/app/history-url.service';
import { Contact } from 'src/app/interfaces';
import { UserService } from 'src/app/user/user.service';
import { AnnuaireService } from '../annuaire.service';

@Component({
  selector: 'app-contact-detail',
  templateUrl: './contact-detail.component.html',
  styleUrls: ['./contact-detail.component.scss']
})
export class ContactDetailComponent implements OnInit {

  contactUUID;
  contact;
  goBackLinkLabel: string;

  constructor(
    private route: ActivatedRoute,
    private annuaireService: AnnuaireService,
    public userService: UserService,
    private historyUrl: HistoryUrlService,
    private _location: Location,
  ) {
    this.goBackLinkLabel = this.historyUrl.getPreviousLabel()
    this.contact = {
      uuid: '',
      first_name: '',
      last_name: '',
      group_name: '',
      position: {
        position: {
          label: ''
        },
        group: {
          label: ''
        }
      },
      tel: {
        mobile: '',
      },
      email: '',
      address: ''
    }
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.contactUUID = params['uuid']
      this.annuaireService.getContactDetails(this.contactUUID).subscribe(contact => {
        this.contact = contact
      })
    })
  }

  addContactToFavorite(contact: Contact) {
    if (this.userService.isUserFav(contact.uuid)) {
      this.userService.removeContactFromUserFavs(contact.uuid).subscribe();
    } else {
      this.userService.addContactToUserFavs(contact.uuid).subscribe();
    }
  }

  goBack(): void {
    this._location.back()
  }

}
