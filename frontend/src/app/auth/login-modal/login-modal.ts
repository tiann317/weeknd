import { Component, EventEmitter, Output, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login-modal',
  imports: [FormsModule],
  templateUrl: './login-modal.html',
  styleUrl: './login-modal.css',
})
export class LoginModal {
  @Output() closed = new EventEmitter<void>();

  private readonly auth = inject(AuthService);

  tab = signal<'login' | 'register'>('login');
  error = signal<string | null>(null);
  loading = signal(false);

  email = '';
  username = '';
  password = '';

  switchTab(tab: 'login' | 'register') {
    this.tab.set(tab);
    this.error.set(null);
  }

  submit() {
    this.error.set(null);
    this.loading.set(true);

    if (this.tab() === 'login') {
      this.auth.login(this.email, this.password).subscribe({
        next: () => {
          this.auth.getMe().subscribe();
          this.closed.emit();
        },
        error: (err) => {
          this.error.set(err.error?.detail ?? 'Login failed');
          this.loading.set(false);
        },
      });
    } else {
      this.auth.register(this.email, this.username, this.password).subscribe({
        next: () => {
          this.auth.login(this.email, this.password).subscribe({
            next: () => {
              this.auth.getMe().subscribe();
              this.closed.emit();
            },
            error: () => {
              this.error.set(null);
              this.loading.set(false);
              this.closed.emit();
            },
          });
        },
        error: (err) => {
          this.error.set(err.error?.detail ?? 'Registration failed');
          this.loading.set(false);
        },
      });
    }
  }
}