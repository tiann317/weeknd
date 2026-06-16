import { Injectable, NgZone } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})

export class Geolocation {
  constructor(private ngZone: NgZone) { }

  getCurrentPosition(): Observable<GeolocationCoordinates> {
    return new Observable(observer => {
      if (!navigator.geolocation) {
        observer.error('Geolocation not supported');
        return;
      }
      navigator.geolocation.getCurrentPosition(
        (position) => {
          this.ngZone.run(() => {
            observer.next(position.coords);
            observer.complete();
            console.log('DEBUG INFO:');
            console.log('Lat:', position.coords.latitude);
            console.log('Lng:', position.coords.longitude);
          });
        }, (error) => this.ngZone.run(() => observer.error(error)),
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0
        }
      );
    });
  }
}
