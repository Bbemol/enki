import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';
import { Message } from 'src/app/interfaces';
import { EvenementsService } from '../../evenements.service';

@Component({
  selector: 'app-filter-messages',
  templateUrl: './filter-messages.component.html',
  styleUrls: ['./filter-messages.component.scss']
})
export class FilterMessagesComponent implements OnInit {

  filterGroup = new FormGroup({
    etablissement: new FormControl(''),
    auteur: new FormControl(''),
    type: new FormControl(''),
  })
  @Input() messages: Message[];
  @Output() closeFilterEvent = new EventEmitter();
  evenementUUID: string;
  etablissementOptions: any[];
  auteursOptions: any[];
  messageTypeOptions: any[];
  constructor(
    private evenementsService: EvenementsService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.evenementUUID = this.evenementsService.selectedEvenementUUID.getValue()
    this.etablissementOptions = [];
    this.auteursOptions = [];
    this.messageTypeOptions = [];
    const event = this.evenementsService.getEvenementByID(this.evenementUUID)
    this.filterGroup.controls.etablissement.setValue(event.filter.etablissement)
    this.filterGroup.controls.auteur.setValue(event.filter.auteur)
    this.filterGroup.controls.type.setValue(event.filter.type)
  }

  closeFilters(): void {
    this.closeFilterEvent.emit();
  }

  ngOnChanges() {
    if(this.messages) {
      this.messages.forEach(message => {
        if (message.creator) {
          if (!this.etablissementOptions.some(item => item.group_id === message.creator.position.group_id)) {
            this.etablissementOptions.push({
              group_id: message.creator.position.group_id,
              group_label: message.creator.position.group.label
            })
          }
  
          if(!this.auteursOptions.some(item => item.auteur_id === message.creator.uuid)) {
            this.auteursOptions.push({
              auteur_id: message.creator.uuid,
              auteur_label: `${message.creator.first_name} ${message.creator.last_name}`
            })
          }
        }

        if(!this.messageTypeOptions.some(item => item.type_id === message.type)) {
          this.messageTypeOptions.push({
            type_id: message.type,
            type_label: message.type_label
          })
        }
      })
    }
  }

  ngOnInit(): void {
  }

  onSubmit(): void {
    this.evenementsService.updateEvenementFilter(this.evenementUUID, this.filterGroup.getRawValue()).subscribe(() => {
      this.closeFilters();
    })
  }

  resetFilters(): void {
    this.evenementsService.updateEvenementFilter(this.evenementUUID, {
      etablissement: '',
      auteur: '',
      type: '',
      fromDatetime: '',
      toDatetime: '',
    }).subscribe(() => {
      this.closeFilters();
    })
  }

}
