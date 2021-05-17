import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { MobilePrototypeService } from 'src/app/mobile-prototype/mobile-prototype.service';
import { MessagesService } from '../messages.service';
import { Message } from 'src/app/interfaces';
import { MESSAGE_INIT } from '../../../constants/message_init';
import { Location } from '@angular/common';

@Component({
  selector: 'app-detail-message',
  templateUrl: './detail-message.component.html',
  styleUrls: ['./detail-message.component.scss']
})
export class DetailMessageComponent implements OnInit {

  messageUUID: string;
  message: Message;

  constructor(
    private messagesService: MessagesService,
    private route: ActivatedRoute,
    public mobilePrototype: MobilePrototypeService,
    private router: Router,
  ) {
    this.message = MESSAGE_INIT;
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      this.messageUUID = params['uuid'];
      this.messagesService.getMessageByID(this.messageUUID).subscribe(message => {
        this.message = message;
      })
    })
  }

  goBack(): void {
    this.router.navigate(['../../'], { relativeTo: this.route });
  }

}
