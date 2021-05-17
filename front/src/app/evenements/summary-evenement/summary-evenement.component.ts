import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import * as L from 'leaflet';
import { BehaviorSubject } from 'rxjs';

import { Affaire, Evenement } from 'src/app/interfaces';
import { EvenementsService } from '../evenements.service';

@Component({
  selector: 'app-summary-evenement',
  templateUrl: './summary-evenement.component.html',
  styleUrls: ['./summary-evenement.component.scss']
})
export class SummaryEvenementComponent implements OnInit {
  map;
  icon;
  evenementUUID: string;
  evenement: Evenement;
  affaires = new BehaviorSubject<Affaire[]>([]);
  uuid;

  constructor(
    private evenementsService: EvenementsService,
    private router: Router,
  ) {
    this.evenementUUID = this.evenementsService.selectedEvenementUUID.getValue()
    this.evenement = this.evenementsService.getEvenementByID(this.evenementUUID);
    this.evenementsService.getEvenementLocationPolygon(this.evenement.location_id).subscribe(data => {
      let eventPolygon = L.polygon(data.geometry.coordinates[0]).addTo(this.map);
      const bounds = eventPolygon.getBounds();
      this.map.fitBounds(bounds);
      this.map.panTo([data.centroid[0], data.centroid[1]])
      this.evenementsService.getSignalementsForEvenement(this.evenement.uuid).subscribe(response => {
        this.affaires.next(response)
      })
    })
  }

  getAffaires(): Affaire[] {
    return this.affaires.getValue();
  }
  ngOnInit(): void {
    this.initMap()
    this.affaires.subscribe((affaires) => {
      this.addMarker()
    })
  }

  addMarker(): void {
    if (this.affaires.getValue().length > 0) {
      this.affaires.getValue().forEach(inter => {
        L.marker([inter.coord.lat, inter.coord.long], {icon: this.icon}).addTo(this.map);
      })
    }
  }
  private initMap(): void {
    this.icon = L.icon({
      iconUrl: 'assets/marker-icon-2x.png',
      iconSize: [32, 32],
      iconAnchor: [16, 32],
    })
    this.map = L.map('map', {
      center: [ 39, -98 ],
      zoom: 10
    })
    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);
  }



  ngAfterViewInit(): void {

  }

  closeEvenement(): void {
    this.evenementsService.closeEvenement(this.evenement.uuid).subscribe((res) => {
      this.router.navigate(['/evenements'])
    })
  }

}
