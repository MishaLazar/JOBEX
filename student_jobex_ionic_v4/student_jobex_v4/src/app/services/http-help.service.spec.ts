import { TestBed } from '@angular/core/testing';

import { HttpHelpService } from './http-help.service';

describe('HttpHelpService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: HttpHelpService = TestBed.get(HttpHelpService);
    expect(service).toBeTruthy();
  });
});
