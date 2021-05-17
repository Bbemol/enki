import { HttpClient } from '@angular/common/http';
import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Observable, Subscription, timer } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { User, MessageFilter, Message } from 'src/app/interfaces';
import { ModalComponent } from 'src/app/ui/modal/modal.component';
import { UserService } from 'src/app/user/user.service';
import { environment } from 'src/environments/environment';
import { EvenementsService } from '../../evenements.service';
import { MessagesService } from '../messages.service';



@Component({
  selector: 'app-liste-main-courante',
  templateUrl: './liste-main-courante.component.html',
  styleUrls: ['./liste-main-courante.component.scss','../../detail-evenement/detail-evenement.component.scss']
})
export class ListeMainCouranteComponent implements OnInit {

  messages: Array<Message>;
  uuid: string;
  fetchedMessages: boolean;
  user: User;
  currentEventFilter: MessageFilter;
  exportType = new FormControl('xlsx');
  messages$: Observable<Message[]>;
  subscription: any;
  showFilters: boolean;
  messageUpdateSubscription: Subscription;

  @ViewChild(ModalComponent) modal: ModalComponent;

  constructor(
    private messagesService: MessagesService,
    private evenementsService: EvenementsService,
    private userService: UserService,
    private router: Router,
    private route: ActivatedRoute,
    private http: HttpClient,
    ) {
      this.messages = []
      this.uuid = this.evenementsService.selectedEvenementUUID.getValue();
    const event = this.evenementsService.getEvenementByID(this.uuid);
    this.currentEventFilter = event.filter;
    this.evenementsService.evenements$.subscribe(() => {
      this.currentEventFilter = this.evenementsService.getEvenementByID(this.uuid).filter;
    })
    this.user = this.userService.user
    this.showFilters = false;
  }

  ngOnInit(): void {
    const timer$ = timer(0, 10000);
    this.messages$ = timer$.pipe(
      switchMap(() => this.messagesService.httpGetMessages(this.uuid))
    )
    this.subscription = this.messages$.subscribe((messages) => {
      this.evenementsService.setMessages(this.uuid, this.messages);
      this.fetchedMessages = true;
      this.messages = messages.sort((a, b) => {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      });
    })
    this.messageUpdateSubscription = this.messagesService.messages$.subscribe(messages => {
      this.messages = messages.sort((a, b) => {
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      });
    })
  }
  ngOnDestroy(): void {
    this.subscription.unsubscribe();
    this.messageUpdateSubscription.unsubscribe();
  }
  addReaction(messageUUID: string): void {
    this.addReactionHttp(messageUUID).subscribe(res => {
      console.log(`Success http result: ${res}`);
    });
  }
  addReactionHttp(messageUUID: string): Observable<any> {
    return this.http.post(`${environment.backendUrl}/events/${this.uuid}/messages/${messageUUID}/react`, {
      reaction: 'ok'
    });
  }
  getCreatorCSSClass(creator: string): string {
    switch (creator) {
      case 'MAIRIE':
        return '-green';
      case 'PREFECTURE':
        return '-blue';
      case 'SDIS':
        return '-red';
    }

  }
  openModal(): void {
    this.modal.open()
  }
  openFilters(): void {
    this.showFilters = true;
  }
  hideFilters(): void {
    this.showFilters = false;
  }
  exportMainCourante(): void {
    this.evenementsService.getMainCouranteData().subscribe(data => {
      const a = document.createElement("a");
      a.style.display = "none";
      document.body.appendChild(a);

      // Set the HREF to a Blob representation of the data to be downloaded
      a.href = window.URL.createObjectURL(
        new Blob([data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;charset=utf-8;' })
      );

      // Use download attribute to set set desired file name
      a.setAttribute("download", `${this.evenementsService.selectedEvenementUUID.getValue()}-${(new Date()).toISOString()}.xlsx`);

      // Trigger the download by simulating click
      a.click();

      // Cleanup
      this.modal.close()
      window.URL.revokeObjectURL(a.href);
      document.body.removeChild(a);
    });
  }

  listIsFiltered(): boolean {
    return Object.keys(this.currentEventFilter).some(element => {
      return this.currentEventFilter[element] !== "";
    })
  }

  clickOnMessage(message: Message): void {
    // routerLink="../detailmessage/{{message.uuid}}"
    if (message.type === 'meeting') {
      // TODO
      // replace window.open by calling joinMeeting in evenementsService and passing meetingID...
      window.open(message.description, '_blank')
    } else {
      this.router.navigate([`./message/${message.uuid}`], { relativeTo: this.route })
    }
  }

}
