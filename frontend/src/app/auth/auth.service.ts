import { Injectable, computed, inject, signal } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';

export interface User {
  id: string;
  email: string;
  username: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
}

interface Token {
  access_token: string;
  token_type: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private readonly http = inject(HttpClient);

  private token = signal<string | null>(localStorage.getItem('token'));
  currentUser = signal<User | null>(null);
  isLoggedIn = computed(() => !!this.token());

  login(email: string, password: string): Observable<Token> {
    const body = new HttpParams().set('username', email).set('password', password);
    return this.http
      .post<Token>(`${environment.apiUrl}/login/access-token`, body, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      .pipe(
        tap((res) => {
          localStorage.setItem('token', res.access_token);
          this.token.set(res.access_token);
        })
      );
  }

  register(email: string, username: string, password: string): Observable<User> {
    return this.http.post<User>(`${environment.apiUrl}/users/signup`, {
      email,
      username,
      password,
    });
  }

  getMe(): Observable<User> {
    return this.http
      .get<User>(`${environment.apiUrl}/users/me`, {
        headers: { Authorization: `Bearer ${this.token()}` },
      })
      .pipe(tap((user) => this.currentUser.set(user)));
  }

  logout(): void {
    localStorage.removeItem('token');
    this.token.set(null);
    this.currentUser.set(null);
  }
}