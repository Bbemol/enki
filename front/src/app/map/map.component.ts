import { Component, Input, OnInit } from '@angular/core';
import * as L from 'leaflet';
import { Affaire } from 'src/app/interfaces';

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.scss']
})
export class MapComponent implements OnInit {
  map;
  icon;
  @Input() affaire: Affaire;

  constructor() {}

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
    this.initMap()
    this.map.panTo([this.affaire.coord.lat, this.affaire.coord.long])
    L.marker([this.affaire.coord.lat, this.affaire.coord.long], {icon: this.icon}).addTo(this.map);
  }

  ngOnInit(): void {
  }

}
