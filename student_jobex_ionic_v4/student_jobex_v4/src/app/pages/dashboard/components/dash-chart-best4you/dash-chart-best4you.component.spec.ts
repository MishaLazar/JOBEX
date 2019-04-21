import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DashChartBest4youComponent } from './dash-chart-best4you.component';

describe('DashChartBest4youComponent', () => {
  let component: DashChartBest4youComponent;
  let fixture: ComponentFixture<DashChartBest4youComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DashChartBest4youComponent ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DashChartBest4youComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
