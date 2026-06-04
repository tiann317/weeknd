import { AfterViewInit, Component, ElementRef, ViewChild, inject, ChangeDetectorRef } from '@angular/core';
import { Map, map, marker, tileLayer } from 'leaflet';
import { Geolocation } from '../geolocation';

@Component({
  selector: 'app-map-simple',
  imports: [],
  templateUrl: './map-simple.html',
  styleUrl: './map-simple.css',
})

export class MapSimple implements AfterViewInit {
  private readonly geolocation: Geolocation = inject(Geolocation);
  private readonly detector: ChangeDetectorRef = inject(ChangeDetectorRef);

  @ViewChild('map')
  mapElementRef: ElementRef = null!;

  public map: Map = null!;

  ngAfterViewInit(): void {

    this.map = map(this.mapElementRef.nativeElement)
      .setView([46.801111, 8.226667], 8);

    tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(this.map);

    this.geolocation.getCurrentPosition().subscribe({
      next: (coords) => {
        this.map.setView([coords.latitude, coords.longitude], 13);
        marker([coords.latitude, coords.longitude], { draggable: true })
          .addTo(this.map).bindPopup('This is me').openPopup()
      },
      error: (err) => console.error('ERROR:', err)
    })
    this.detector.markForCheck();
  }
}
