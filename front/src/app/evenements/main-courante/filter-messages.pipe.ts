import { Pipe, PipeTransform } from '@angular/core';
import { MessageFilter, Message } from 'src/app/interfaces';

@Pipe({
  name: 'filterMessages'
})
export class FilterMessagesPipe implements PipeTransform {

  transform(messages: Message[], filter: MessageFilter, ...args: any[]): unknown {
    // Établissement : messages.filter(message => message.creator.position.group_id === "61b7324b-632f-4f22-bc5e-f288117c74fe"
    // Type de message : messages.filter(message => message.type === "meeting")
    // 
    // return messages.filter(message => message.creator.position.group_id === "61b7324b-632f-4f22-bc5e-f288117c74fe")
    // return messages.filter(message => message.creator.uuid === '75d9bc1d-207f-4cc2-8d40-ef420739d128')
    if (!messages || messages.length === 0) return [];
    const isEmpty = !Object.values(filter).some(x => (x !== null && x !== '')) ? messages : null;

    return isEmpty ? messages : messages.filter(message => {
      if (!message.creator) return false;
      return (
        filter.etablissement && filter.etablissement === message.creator.position.group_id
        || filter.auteur && filter.auteur === message.creator.uuid
        || filter.type && filter.type === message.type
      );
    });
  }

}
