import { AfterViewInit, Component, ElementRef, ViewChild, inject, ChangeDetectorRef, signal } from '@angular/core';
import { LayerGroup, Map, layerGroup, map, marker, tileLayer } from 'leaflet';
import { Geolocation } from '../geolocation';
import { AuthService } from '../auth/auth.service';
import { LoginModal } from '../auth/login-modal/login-modal';
import { HikeService } from '../hike/hike.service';
import { HikeDetail, HikeListItem } from '../hike/hike.models';

@Component({
  selector: 'app-map-simple',
  imports: [LoginModal],
  templateUrl: './map-simple.html',
  styleUrl: './map-simple.css',
})

export class MapSimple implements AfterViewInit {
  private readonly geolocation: Geolocation = inject(Geolocation);
  private readonly detector: ChangeDetectorRef = inject(ChangeDetectorRef);
  private readonly hikeService: HikeService = inject(HikeService);
  readonly auth = inject(AuthService);

  showLoginModal = signal(false);
  selected = signal<HikeDetail | null>(null);
  region = signal<string | null>(null);
  preset = ["Garmisch", "Kochel", "Ammersee"];

  private hikeLayer: LayerGroup = layerGroup();

  @ViewChild('map')
  mapElementRef: ElementRef = null!;

  public map: Map = null!;

  loadHikes() {
    this.hikeService.list(this.region() ?? undefined).subscribe(h => this.drawHikes(h))
  }

  onRegionChange(r: string | null) {
    this.region.set(r);
    this.loadHikes();
  }

  drawHikes(hikes: HikeListItem[]) {
    this.hikeLayer.clearLayers();
    for (const h of hikes) {
      marker([h.start_lat, h.start_lon])
        .bindTooltip(h.title)
        .on('click', () => this.hikeService.get(h.id).subscribe(d => this.selected.set(d)))
        .addTo(this.hikeLayer);
    }
  }

  loadNearby() {
    this.geolocation.getCurrentPosition().subscribe({
      next: (c) => {
        this.map.setView([c.latitude, c.longitude], 11);
        this.hikeService.nearby(c.latitude, c.longitude).subscribe(h => this.drawHikes(h));
      },
      error: (err) => console.error('ERROR:', err),
    });
  }

  ngAfterViewInit(): void {

    this.map = map(this.mapElementRef.nativeElement)
      .setView([46.801111, 8.226667], 8);

    this.map.attributionControl.setPrefix(false);
    tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(this.map);

    this.hikeLayer.addTo(this.map);

    this.loadHikes();

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
