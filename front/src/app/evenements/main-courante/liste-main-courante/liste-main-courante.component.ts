import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { User } from 'src/app/interfaces/User';
import { UserService } from 'src/app/user/user.service';
import { EvenementsService } from '../../evenements.service';
import { Message, MessagesService } from '../messages.service';

@Component({
  selector: 'app-liste-main-courante',
  templateUrl: './liste-main-courante.component.html',
  styleUrls: ['./liste-main-courante.component.scss']
})
export class ListeMainCouranteComponent implements OnInit {

  messages: Array<Message>;
  uuid: string;
  fetchedMessages: boolean;
  user: User;
  constructor(
    private messagesService: MessagesService,
    private evenementsService: EvenementsService,
    private userService: UserService
    ) {
    this.messages = []
    this.uuid = this.evenementsService.selectedEvenement.uuid
    this.user = this.userService.user
  }

  ngOnInit(): void {
    this.messagesService.getMessagesByEvenementID(this.uuid).subscribe(messages => {
      this.messages = messages.sort((a, b) => {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      })
      this.fetchedMessages = true
    })
  }

}
