import { Pipe, PipeTransform } from '@angular/core';
import { Contact } from 'src/app/interfaces'

@Pipe({
  name: 'searchContact'
})
export class SearchContactPipe implements PipeTransform {

  transform(contacts: Contact[], ...args: any): any {
    return contacts.filter(contact => {
      return contact.first_name.toLowerCase().indexOf(args[0].toLowerCase()) !== -1
    });
  }

}
