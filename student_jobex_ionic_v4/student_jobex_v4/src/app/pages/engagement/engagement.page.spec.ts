import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EngagementPage } from './engagement.page';

describe('EngagementPage', () => {
  let component: EngagementPage;
  let fixture: ComponentFixture<EngagementPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EngagementPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EngagementPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
