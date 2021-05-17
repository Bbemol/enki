import { Component, OnInit, ViewChild } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { MessagesService } from '../messages.service';
import { LabelsService } from '../labels.service';
import { EvenementsService } from '../../evenements.service';
import { ModalComponent } from 'src/app/ui/modal/modal.component';
import { Observable, Subject } from 'rxjs';

const TITLE_MAX_LENGTH = 150;
const TITLE_MIN_LENGTH = 2;

interface Media {
  uuid: string;
  url: string;
}

enum MessageType {
  PUBLIC = 'public',
  RESTRICTED = 'restricted'
}
@Component({
  selector: 'app-add-message',
  templateUrl: './add-message.component.html',
  styleUrls: ['./add-message.component.scss']
})
export class AddMessageComponent implements OnInit {
  messageGroup = new FormGroup({
    title: new FormControl('', [
      Validators.required,
      Validators.minLength(TITLE_MIN_LENGTH),
      Validators.maxLength(TITLE_MAX_LENGTH),
    ]),
    content: new FormControl(''),
    files: new FormControl('')
  })
  messageType = MessageType;
  evenementUUID: string;
  listOfMedias: Array<Media>;
  formSubmitted: boolean;
  charactersTitleLimit: number;
  textareaLength: number;
  public confirmButton = new Subject<boolean>();
  public confirmBtn$ = this.confirmButton.asObservable();
  @ViewChild('confirmation') modal: ModalComponent;
  @ViewChild('cancel') modalCancel: ModalComponent;
  constructor(
    private messagesService: MessagesService,
    public labelsService: LabelsService,
    private evenementsService: EvenementsService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.listOfMedias = [];
    this.formSubmitted = false;
    this.charactersTitleLimit = TITLE_MAX_LENGTH;
    this.textareaLength = 0;
    this.messageGroup.controls.title.valueChanges.subscribe((value: string) => {
      this.textareaLength = value.length;
    })
  }

  get title() { return this.messageGroup.get('title'); }

  close(): void {
    this.router.navigate(['..'], { relativeTo: this.route });
  }
  onSubmit(messageType: MessageType): void {
    let selectedLabelsUUID = this.labelsService.selectedLabels.map(label => label.uuid)
    this.evenementUUID = this.evenementsService.selectedEvenementUUID.getValue()
    this.messagesService.httpSubmitMessage(
        this.messageGroup.value.title,
        this.messageGroup.value.content,
        selectedLabelsUUID,
        this.evenementUUID,
        this.listOfMedias.map(media => media.uuid),
        messageType === MessageType.RESTRICTED ? true : false
      ).subscribe(() => {
        this.formSubmitted = true;
        this.router.navigate([`..`], { relativeTo: this.route })
      }
    )
  }

  openConfirmationModal(): void {
    this.modal.open()
  }
  closeCancelModal(): void {
    this.modalCancel.close()
  }

  uploadFile(event: any): void {
    // TODO : montrer le loader
    const file = (event.target as HTMLInputElement).files[0]
    this.messagesService.getUrlFileUpload((event.target as HTMLInputElement).files[0]).subscribe(response => {
      this.messagesService.putFileOnServer(file, response.data.upload_url).subscribe(() => {
        // TODO : cacher le loader
        // montrer l'image de preview
        let mediaUUID = response.data.uuid
        this.messagesService.getUrlFileDownload(mediaUUID).subscribe(minioDataObj => {
          this.listOfMedias.push({uuid: mediaUUID, url: minioDataObj.data.url})
        })
      })
    })
  }

  removeMedia(mediaUUID: string): void {
    this.messagesService.removeFileFromServer(mediaUUID).subscribe(response => {
      if (response.message === 'success') {
        this.listOfMedias = this.listOfMedias.filter(media => media.uuid !== mediaUUID)
      }
    })
  }

  canDeactivate(): Observable<any> | boolean {
    if (this.formSubmitted) return true;
    for (const property in this.messageGroup.value ) {
      if (this.messageGroup.value[property] !== '') {
        this.modalCancel.open()
        return this.confirmBtn$;
      }
    }
    return true;
  }

  ngOnDestroy(): void {
    this.labelsService.selectedLabels = []
  }

  ngOnInit(): void {
  }

}
