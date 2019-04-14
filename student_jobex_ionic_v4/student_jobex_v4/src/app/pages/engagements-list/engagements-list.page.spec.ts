import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { EngagementsListPage } from './engagements-list.page';

describe('EngagementsListPage', () => {
  let component: EngagementsListPage;
  let fixture: ComponentFixture<EngagementsListPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ EngagementsListPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(EngagementsListPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
