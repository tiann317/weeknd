import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  template: `
  <main class="container page">
      <p class="my-4 text-lg text-body">FastAPI + Angular + PostgreSQL. Made by Ivan Titov.</p>
      <section class="content">
        <router-outlet />
      </section>
    </main>
  `,
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}

