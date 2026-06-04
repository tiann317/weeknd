import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MapSimple } from './map-simple';

describe('MapSimple', () => {
  let component: MapSimple;
  let fixture: ComponentFixture<MapSimple>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MapSimple],
    }).compileComponents();

    fixture = TestBed.createComponent(MapSimple);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
