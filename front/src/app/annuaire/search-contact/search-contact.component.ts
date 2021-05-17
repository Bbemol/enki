import { Component, OnInit } from '@angular/core';
import { Contact } from 'src/app/interfaces';
import { AnnuaireService } from '../annuaire.service';
import { FormControl } from '@angular/forms';
import { UserService } from 'src/app/user/user.service';
import { interval, Observable, Subject } from 'rxjs';
import { debounce, switchMap } from 'rxjs/operators';
import { SEARCH_MIN_CHARS } from 'src/app/constants/constants';
import { HighlightIncludedCharsPipe } from 'src/app/highlight-included-chars.pipe';

@Component({
  selector: 'app-search-contact',
  templateUrl: './search-contact.component.html',
  styleUrls: ['./search-contact.component.scss'],
  providers: [HighlightIncludedCharsPipe]
})
export class SearchContactComponent implements OnInit {

  contactList: Contact[];
  contactSearch = new FormControl('');
  subject = new Subject();
  contactResult$: Observable<Contact[]>;
  

  constructor(
    private annuaireService: AnnuaireService,
    public userService: UserService,
    private highlightTransform: HighlightIncludedCharsPipe,
  ) {
    this.contactList = []
    this.contactSearch.valueChanges.subscribe(value => {
      if (value.length >= SEARCH_MIN_CHARS) {
        this.subject.next(value)
      }
    });
    this.contactResult$ = this.subject.pipe(
      debounce(() => interval(500)),
      switchMap((query: string) => {
        return this.annuaireService.searchInAnnuaire(query)
      })
    )

    this.contactResult$.subscribe(contacts => {
      this.contactList = contacts;
    })
  }

  ngOnInit(): void {
  }

  getContactLabel(contact: Contact, searchvalue: string): string {
    const firstName = this.highlightTransform.transform(contact.first_name, searchvalue)
    const lastName = this.highlightTransform.transform(contact.last_name, searchvalue)

    return `${firstName} ${lastName}`
  }

  addRemoveToUserFavs(contactId: string): void {
    if (this.userService.user.contacts.filter(contact => contact.uuid === contactId).length > 0) {
      this.userService.removeContactFromUserFavs(contactId).subscribe()
    } else {
      this.userService.addContactToUserFavs(contactId).subscribe()
    }
  }

  isUserFav(contactId: string): boolean {
    return this.userService.isUserFav(contactId)
  }
}
