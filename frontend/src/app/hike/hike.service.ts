import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { HikeDetail, HikeListItem } from './hike.models';

@Injectable({ providedIn: 'root' })
export class HikeService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiUrl}/hikes`;

  list(region?: string): Observable<HikeListItem[]> {
    let params = new HttpParams();
    if (region) {
      params = params.set('region', region);
    }
    return this.http.get<HikeListItem[]>(this.base, { params });
  }

  get(id: string): Observable<HikeDetail> {
    return this.http.get<HikeDetail>(`${this.base}/${id}`);
  }
}
